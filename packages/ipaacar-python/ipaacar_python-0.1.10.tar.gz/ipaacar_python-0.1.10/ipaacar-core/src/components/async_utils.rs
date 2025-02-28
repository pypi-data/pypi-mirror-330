use crate::backend::Backend;
use crate::components::buffer::buffer_iu_cb_manager::IUCallbackManager;
use crate::components::callback_list::CallbackList;
use crate::components::iu::core::IUCore;
use crate::components::iu::IU;
use log::{error, info};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{Mutex, RwLock};

/// This function is the deserialization and replacement logic for IU cores.
pub(crate) async fn iu_updater_routine<B: Backend + Sync + Send + 'static>(
    data: Vec<u8>,
    iu: Arc<IU<B>>,
) {
    let new_core_ds = rmp_serde::from_slice(&data);
    match new_core_ds {
        Ok(new_core) => {
            iu.update_iu_core(new_core).await;
        }
        Err(e) => {
            error!(
                "Received invalid IU update. Deserialization Failed Ignoring. Error:\n{}",
                e.to_string()
            );
        }
    }
}

/// This function processes incoming IUs and determines if they are new or not.
/// Used by the InputBuffer listener.
pub(crate) async fn handle_data_to_new_iu<B: Backend + Sync + Send + 'static>(
    data: Vec<u8>,
    component_name: String,
    received_ius: Arc<RwLock<HashMap<String, Arc<IU<B>>>>>,
    callback_manager: Arc<Mutex<IUCallbackManager<B>>>,
    backend: Arc<B>,
    new_iu_callbacks: Arc<Mutex<CallbackList<Arc<IU<B>>>>>,
) {
    let iu_core_res: Result<IUCore, _> = rmp_serde::from_slice(&data);
    match iu_core_res {
        Ok(iu_core) => {
            let received_ius_rg = received_ius.read().await;
            let contains_iu = received_ius_rg.contains_key(&iu_core.uid);
            drop(received_ius_rg);
            if !contains_iu {
                info!("new IU {} received in Input Buffer", &iu_core.uid);
                let backend = Arc::clone(&backend);
                let uid = iu_core.uid.clone();
                let iu = IU::from_core(iu_core, None, backend);
                let new_iu = Arc::clone(&iu);
                let mut ius = received_ius.write().await;
                ius.insert(uid.clone(), iu);
                drop(ius);
                let mut cbm = callback_manager.lock().await;
                let add_res = cbm.add_iu_updater(&component_name, &uid).await;
                drop(cbm);
                if add_res.is_err() {
                    error!(
                        "Adding updater for IU {} failed. IU will be removed again.",
                        &uid
                    );
                    let mut ius = received_ius.write().await;
                    ius.remove(&uid);
                } else {
                    let iu_cbs = new_iu_callbacks.lock().await;
                    iu_cbs.call(new_iu).await;
                }
            }
        }
        Err(e) => {
            error!(
                "Received invalid IU update. Deserialization Failed Ignoring. Error:\n{}",
                e.to_string()
            );
        }
    }
}

pub(crate) async fn handle_new_msg(
    data: Vec<u8>,
    new_message_callbacks: Arc<Mutex<CallbackList<String>>>,
) {
    let message = String::from_utf8(data);
    match message {
        Ok(m) => {
            let cbs = new_message_callbacks.lock().await;
            cbs.call(m).await;
        }
        Err(_) => {
            error!("Received Message with invalid encoding.");
        }
    }
}
