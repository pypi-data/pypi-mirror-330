use crate::backend::Backend;

use crate::components::async_utils::iu_updater_routine;
use crate::components::iu::IU;
use crate::VoidOrAsyncError;
use log::error;
use std::collections::HashMap;
use std::sync::Arc;
use thiserror::Error;
use tokio::sync::RwLock;
use uuid::Uuid;

/// responsible for listeners
pub(crate) struct IUCallbackManager<B: Backend + Sync + Send> {
    backend: Arc<B>,
    ius: Arc<RwLock<HashMap<String, Arc<IU<B>>>>>,
    /// iu uid and a string as a callback id
    updater: HashMap<String, String>,
}

impl<B: Backend + Sync + Send + 'static> IUCallbackManager<B> {
    pub fn new(backend: Arc<B>, ius: Arc<RwLock<HashMap<String, Arc<IU<B>>>>>) -> Self {
        Self {
            backend,
            ius,
            updater: Default::default(),
        }
    }

    pub async fn add_iu_updater(&mut self, component: &str, iu_id: &str) -> VoidOrAsyncError {
        if self.updater.contains_key(iu_id) {
            return Err(Box::new(IUCallbackManagerError::UpdaterForIUAlreadyAdded));
        }
        let ius = self.ius.read().await;
        if let Some(iu) = ius.get(iu_id) {
            let category = iu.get_category().await;
            let iu = Arc::clone(iu);
            drop(ius);
            let cb = move |data: Vec<u8>| iu_updater_routine(data, Arc::clone(&iu));

            let callback_id = Uuid::new_v4().to_string();

            self.backend
                .add_callback(
                    format!("{}/{}/IU/{}", component, category, iu_id),
                    callback_id,
                    cb,
                )
                .await?;
            Ok(())
        } else {
            Err(Box::new(IUCallbackManagerError::IUNotInBuffer))
        }
    }
}

#[derive(Error, Debug)]
pub enum IUCallbackManagerError {
    #[error("a listener was already added for the IU")]
    UpdaterForIUAlreadyAdded,
    #[error("Couldn't find IU in buffer")]
    IUNotInBuffer,
}
