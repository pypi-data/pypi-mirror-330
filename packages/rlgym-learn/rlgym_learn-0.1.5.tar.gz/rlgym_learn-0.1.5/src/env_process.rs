use pyany_serde::communication::{append_bool, append_usize};
use pyany_serde::{DynPyAnySerdeOption, PyAnySerde};
use pyo3::exceptions::asyncio::InvalidStateError;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};
use pyo3::{intern, PyAny, Python};
use raw_sync::events::{Event, EventInit, EventState};
use raw_sync::Timeout;
use shared_memory::ShmemConf;
use std::thread::sleep;
use std::time::Duration;

use crate::env_action::{retrieve_env_action, EnvAction};
use crate::synchronization::{get_flink, recvfrom_byte, retrieve_header, sendto_byte, Header};

fn sync_with_epi<'py>(socket: &Bound<'py, PyAny>, address: &Bound<'py, PyAny>) -> PyResult<()> {
    sendto_byte(socket, address)?;
    recvfrom_byte(socket)?;
    Ok(())
}

fn env_reset<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<Bound<'py, PyDict>> {
    Ok(env
        .call_method0(intern!(env.py(), "reset"))?
        .downcast_into()?)
}

fn env_set_state<'py>(
    env: &'py Bound<'py, PyAny>,
    desired_state: &Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyDict>> {
    Ok(env
        .call_method1(intern!(env.py(), "set_state"), (desired_state,))?
        .downcast_into()?)
}

fn env_render<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<()> {
    env.call_method0(intern!(env.py(), "render"))?;
    Ok(())
}

fn env_state<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
    env.getattr(intern!(env.py(), "state"))
}

fn env_shared_info<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> {
    env.getattr(intern!(env.py(), "shared_info"))
}

fn env_obs_spaces<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<Bound<'py, PyDict>> {
    Ok(env
        .getattr(intern!(env.py(), "observation_spaces"))?
        .downcast_into()?)
}

fn env_action_spaces<'py>(env: &'py Bound<'py, PyAny>) -> PyResult<Bound<'py, PyDict>> {
    Ok(env
        .getattr(intern!(env.py(), "action_spaces"))?
        .downcast_into()?)
}

fn env_step<'py>(
    env: &'py Bound<'py, PyAny>,
    actions_dict: Bound<'py, PyDict>,
) -> PyResult<(
    Bound<'py, PyDict>,
    Bound<'py, PyDict>,
    Bound<'py, PyDict>,
    Bound<'py, PyDict>,
)> {
    let result: Bound<'py, PyTuple> = env
        .call_method1(intern!(env.py(), "step"), (actions_dict,))?
        .downcast_into()?;
    Ok((
        result.get_item(0)?.downcast_into()?,
        result.get_item(1)?.downcast_into()?,
        result.get_item(2)?.downcast_into()?,
        result.get_item(3)?.downcast_into()?,
    ))
}

#[pyfunction]
#[pyo3(signature=(proc_id,
    child_end,
    parent_sockname,
    build_env_fn,
    flinks_folder,
    shm_buffer_size,
    agent_id_serde,
    action_serde,
    obs_serde,
    reward_serde,
    obs_space_serde,
    action_space_serde,
    state_serde_option,
    state_metrics_serde_option,
    collect_state_metrics_fn_option,
    send_state_to_agent_controllers=false,
    render=false,
    render_delay_option=None,
    recalculate_agent_id_every_step=false))]
pub fn env_process<'py>(
    proc_id: &str,
    child_end: Bound<'py, PyAny>,
    parent_sockname: Bound<'py, PyAny>,
    build_env_fn: Bound<'py, PyAny>,
    flinks_folder: &str,
    shm_buffer_size: usize,
    agent_id_serde: Box<dyn PyAnySerde>,
    action_serde: Box<dyn PyAnySerde>,
    obs_serde: Box<dyn PyAnySerde>,
    reward_serde: Box<dyn PyAnySerde>,
    obs_space_serde: Box<dyn PyAnySerde>,
    action_space_serde: Box<dyn PyAnySerde>,
    state_serde_option: DynPyAnySerdeOption,
    state_metrics_serde_option: DynPyAnySerdeOption,
    collect_state_metrics_fn_option: Option<Bound<'py, PyAny>>,
    send_state_to_agent_controllers: bool,
    render: bool,
    render_delay_option: Option<Duration>,
    recalculate_agent_id_every_step: bool,
) -> PyResult<()> {
    if send_state_to_agent_controllers && matches!(state_serde_option, DynPyAnySerdeOption::None) {
        return Err(PyValueError::new_err(
            "state_serde must be passed in order to send state to agent controllers",
        ));
    }
    if collect_state_metrics_fn_option.is_some()
        && matches!(state_metrics_serde_option, DynPyAnySerdeOption::None)
    {
        return Err(PyValueError::new_err(
                    "state_metrics_serde must be passed in order to collect state metrics from env processes",
                ));
    }
    let state_serde_option: Option<Box<dyn PyAnySerde>> = state_serde_option.into();
    let state_serde_option = state_serde_option.as_ref();
    let state_metrics_serde_option: Option<Box<dyn PyAnySerde>> = state_metrics_serde_option.into();
    let state_metrics_serde_option = state_metrics_serde_option.as_ref();
    let flink = get_flink(flinks_folder, proc_id);
    let mut shmem = ShmemConf::new()
        .size(shm_buffer_size)
        .flink(flink.clone())
        .create()
        .map_err(|err| {
            InvalidStateError::new_err(format!("Unable to create shmem flink {}: {}", flink, err))
        })?;
    let (epi_evt, used_bytes) = unsafe {
        Event::new(shmem.as_ptr(), true).map_err(|err| {
            InvalidStateError::new_err(format!(
                "Failed to create event from epi to this process: {}",
                err.to_string()
            ))
        })?
    };
    let shm_slice = unsafe { &mut shmem.as_slice_mut()[used_bytes..] };

    Python::with_gil::<_, PyResult<()>>(|py| {
        // Initial setup
        let env = build_env_fn.call0()?;
        let mut game_speed_fn: Box<dyn Fn() -> PyResult<f64>> = Box::new(|| Ok(1.0));
        let mut game_paused_fn: Box<dyn Fn() -> PyResult<bool>> = Box::new(|| Ok(false));
        if render {
            let rlviser = PyModule::import(py, "rlviser_py")?;
            let get_game_speed = rlviser.getattr("get_game_speed")?;
            let get_game_paused = rlviser.getattr("get_game_paused")?;
            game_speed_fn = Box::new(move || Ok(get_game_speed.call0()?.extract::<f64>()?));
            game_paused_fn = Box::new(move || Ok(get_game_paused.call0()?.extract::<bool>()?));
        }

        let collect_state_metrics_fn_option = collect_state_metrics_fn_option.as_ref();

        // Startup complete
        sync_with_epi(&child_end, &parent_sockname)?;

        let reset_obs = env_reset(&env)?;
        let should_collect_state_metrics = !collect_state_metrics_fn_option.is_none();
        let mut n_agents = reset_obs.len();
        let mut agent_id_list = Vec::with_capacity(n_agents);
        for agent_id in reset_obs.keys().iter() {
            agent_id_list.push(agent_id);
        }

        // Write reset message
        let mut offset = 0;
        offset = append_usize(shm_slice, offset, n_agents);
        for agent_id in agent_id_list.iter() {
            offset = agent_id_serde.append(shm_slice, offset, agent_id)?;
            offset = obs_serde.append(
                shm_slice,
                offset,
                &reset_obs
                    .get_item(agent_id)?
                    .ok_or(InvalidStateError::new_err(
                        "Reset obs python dict did not contain AgentID as key",
                    ))?,
            )?;
        }

        if send_state_to_agent_controllers {
            _ = state_serde_option
                .unwrap()
                .append(shm_slice, offset, &env_state(&env)?)?;
        }
        sendto_byte(&child_end, &parent_sockname)?;

        // Start main loop
        let mut has_received_env_action = false;
        loop {
            epi_evt
                .wait(Timeout::Infinite)
                .map_err(|err| InvalidStateError::new_err(err.to_string()))?;
            epi_evt
                .set(EventState::Clear)
                .map_err(|err| InvalidStateError::new_err(err.to_string()))?;
            offset = 0;
            let header;
            (header, offset) = retrieve_header(shm_slice, offset)?;
            match header {
                Header::EnvAction => {
                    has_received_env_action = true;
                    let env_action;
                    (env_action, _) = retrieve_env_action(
                        py,
                        shm_slice,
                        offset,
                        agent_id_list.len(),
                        &action_serde,
                        &state_serde_option,
                    )?;
                    // Read actions message
                    let (
                        obs_dict,
                        rew_dict_option,
                        terminated_dict_option,
                        truncated_dict_option,
                        is_step_action,
                    );
                    match &env_action {
                        EnvAction::STEP { action_list, .. } => {
                            let mut actions_kv_list = Vec::with_capacity(agent_id_list.len());
                            let action_list = action_list.bind(py);
                            for (agent_id, action) in agent_id_list.iter().zip(action_list.iter()) {
                                actions_kv_list.push((agent_id, action));
                            }
                            let actions_dict =
                                PyDict::from_sequence(&actions_kv_list.into_pyobject(py)?)?;
                            let (rew_dict, terminated_dict, truncated_dict);
                            (obs_dict, rew_dict, terminated_dict, truncated_dict) =
                                env_step(&env, actions_dict)?;
                            rew_dict_option = Some(rew_dict);
                            terminated_dict_option = Some(terminated_dict);
                            truncated_dict_option = Some(truncated_dict);
                            is_step_action = true;
                        }
                        EnvAction::RESET {} => {
                            obs_dict = env_reset(&env)?;
                            rew_dict_option = None;
                            terminated_dict_option = None;
                            truncated_dict_option = None;
                            is_step_action = false;
                        }
                        EnvAction::SET_STATE { desired_state, .. } => {
                            obs_dict = env_set_state(&env, desired_state.bind(py))?;
                            rew_dict_option = None;
                            terminated_dict_option = None;
                            truncated_dict_option = None;
                            is_step_action = false;
                        }
                    }
                    let new_episode = !is_step_action;

                    if new_episode {
                        n_agents = obs_dict.len();
                    }

                    // Write env step message
                    offset = 0;
                    if new_episode {
                        offset = append_usize(shm_slice, offset, n_agents);
                    }
                    for agent_id in agent_id_list.iter() {
                        if recalculate_agent_id_every_step || new_episode {
                            offset = agent_id_serde.append(shm_slice, offset, agent_id)?;
                        }
                        offset = obs_serde.append(
                            shm_slice,
                            offset,
                            &obs_dict.get_item(agent_id)?.unwrap(),
                        )?;
                        if is_step_action {
                            offset = reward_serde.append(
                                shm_slice,
                                offset,
                                &rew_dict_option
                                    .as_ref()
                                    .unwrap()
                                    .get_item(agent_id)?
                                    .unwrap(),
                            )?;
                            offset = append_bool(
                                shm_slice,
                                offset,
                                terminated_dict_option
                                    .as_ref()
                                    .unwrap()
                                    .get_item(agent_id)?
                                    .unwrap()
                                    .extract::<bool>()?,
                            );
                            offset = append_bool(
                                shm_slice,
                                offset,
                                truncated_dict_option
                                    .as_ref()
                                    .unwrap()
                                    .get_item(agent_id)?
                                    .unwrap()
                                    .extract::<bool>()?,
                            );
                        }
                    }

                    if send_state_to_agent_controllers {
                        offset = state_serde_option.unwrap().append(
                            shm_slice,
                            offset,
                            &env_state(&env)?,
                        )?;
                    }

                    if should_collect_state_metrics {
                        let state_metrics = collect_state_metrics_fn_option
                            .unwrap()
                            .call1((env_state(&env)?, env_shared_info(&env)?))?;
                        _ = state_metrics_serde_option.unwrap().append(
                            shm_slice,
                            offset,
                            &state_metrics,
                        )?;
                    }
                    sendto_byte(&child_end, &parent_sockname)?;

                    // Render
                    if render {
                        env_render(&env)?;
                        if let Some(render_delay) = render_delay_option {
                            sleep(Duration::from_micros(
                                ((render_delay.as_micros() as f64) * game_speed_fn()?).round()
                                    as u64,
                            ));
                        }
                        while game_paused_fn()? {
                            sleep(Duration::from_millis(100));
                        }
                    }
                }
                Header::EnvShapesRequest => {
                    if has_received_env_action {
                        println!("This env process (proc id {:?}) received request for env shapes, but this seems abnormal. Terminating...", proc_id);
                        break;
                    }
                    let obs_space = env_obs_spaces(&env)?.values().get_item(0)?;
                    let action_space = env_action_spaces(&env)?.values().get_item(0)?;
                    println!("Received request for env shapes, returning:");
                    println!("- Observation space type: {}", obs_space.repr()?);
                    println!("- Action space type: {}", action_space.repr()?);
                    println!("--------------------");

                    offset = 0;
                    offset = obs_space_serde.append(shm_slice, offset, &obs_space)?;
                    action_space_serde.append(shm_slice, offset, &action_space)?;
                    sendto_byte(&child_end, &parent_sockname)?;
                }
                Header::Stop => {
                    break;
                }
            }
        }
        Ok(())
    })
}
