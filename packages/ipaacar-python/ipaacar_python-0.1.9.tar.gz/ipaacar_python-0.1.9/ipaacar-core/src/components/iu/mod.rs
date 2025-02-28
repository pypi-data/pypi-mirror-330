use std::collections::HashMap;
use std::fmt::{Display, Formatter};
use std::sync::{Arc, Weak};
use std::time::Duration;

use log::{debug, error};
use tokio::sync::RwLock;
use uuid::Uuid;

use crate::backend::Backend;
use crate::components::callback_list::CallbackList;
use crate::components::iu::core::{IUCore, IUCoreError};
use crate::{CallbackFuture, VoidOrAsyncError};

pub mod core;
pub(crate) mod links;

/// Wrapper around the Core IU with a backend to announce any changes.
/// Takes no mutable references and uses exclusively dynamic ownership management with a mutex lock.
/// This is necessary, because any callbacks might try to access the core IU as well.
/// For this reason, if you change this code, ALWAYS drop the MutexGuard before announcing changes,
/// or you can Deadlock.
pub struct IU<B: Backend + Send + Sync> {
    core: RwLock<IUCore>,
    backend: Arc<B>,
    default_channel: String,
    uid: String,
    update_callbacks: RwLock<CallbackList<Arc<Self>>>,
    cb_ref: Weak<Self>,
}

impl<B: Backend + Send + Sync> IU<B> {
    ///////////////////////////////////////////
    // Constructors
    ///////////////////////////////////////////
    pub fn new(
        category: impl Into<String>,
        component_name: impl Into<String>,
        owner_buffer_uid: impl Into<String>,
        payload: serde_json::Value,
        backend: Arc<B>,
    ) -> Arc<Self> {
        let uid = Uuid::new_v4().to_string();
        let component_name = component_name.into();
        let owner_buffer_uid = owner_buffer_uid.into();
        let category = category.into();
        let default_channel = format!("{}/{}/IU/{}", component_name, &category, &uid);
        let update_callbacks = RwLock::new(CallbackList::new());

        Arc::new_cyclic(|w| Self {
            core: RwLock::new(IUCore::new(
                category,
                component_name,
                Some(owner_buffer_uid),
                payload,
                uid.clone(),
            )),
            backend,
            default_channel,
            uid,
            update_callbacks,
            cb_ref: Weak::clone(w),
        })
    }

    pub fn from_core(
        mut core: IUCore,
        owner_buffer_uid: Option<String>,
        backend: Arc<B>,
    ) -> Arc<Self> {
        let uid = core.uid.clone();
        if let Some(bid) = owner_buffer_uid {
            core.owner_buffer_uid = Some(bid)
        }
        let default_channel = format!("{}/{}/IU/{}", &core.component_name, &core.category, &uid);
        let core = RwLock::new(core);
        let update_callbacks = RwLock::new(CallbackList::new());
        Arc::new_cyclic(|w| Self {
            core,
            backend,
            default_channel,
            uid,
            update_callbacks,
            cb_ref: Weak::clone(w),
        })
    }

    ///////////////////////////////////////////
    // Wrapper specific
    ///////////////////////////////////////////

    /// This should be called by the update callback from the backend
    pub(crate) async fn update_iu_core(&self, new: IUCore) {
        let mut core_locked = self.core.write().await;
        *core_locked = new;
        debug!("IU {} updated", &core_locked.uid);
        drop(core_locked);
        let update_callbacks = self.update_callbacks.read().await;
        match self.cb_ref.upgrade() {
            Some(iu) => update_callbacks.call(iu).await,
            None => error!("Callbacks triggered for non existent IU. This should never happen."),
        }
    }

    pub async fn get_uid(&self) -> &str {
        &self.uid
    }

    pub async fn on_update<F>(&self, cb: F)
    where
        F: Fn(Arc<Self>) -> CallbackFuture<()>,
        F: Send + Sync + 'static,
    {
        let mut update_callbacks = self.update_callbacks.write().await;
        update_callbacks.push(cb);
    }

    ///////////////////////////////////////////
    // Core functionality
    ///////////////////////////////////////////

    /// Commits this IU. Can (or should) only be done by the owner of the IU.
    /// Is checked via a passed id, which might make misuse possible.
    ///
    /// Returns IU::CommittedByNonOwner if buffer_id is not the owner.
    pub async fn commit(&self, buffer_id: &str) -> VoidOrAsyncError {
        let mut core_locked = self.core.write().await;
        let commit = core_locked.commit(buffer_id).await;
        drop(core_locked);
        if commit.is_ok() {
            self.announce_change_over_backend().await?;
        }
        commit
    }

    ///////////////////////////////////////////
    // Core Getters
    //
    // Need to:
    // Lock Core
    ///////////////////////////////////////////

    pub async fn is_committed(&self) -> bool {
        let core_locked = self.core.read().await;
        core_locked.is_committed
    }

    pub async fn get_payload(&self) -> serde_json::Value {
        let core_locked = self.core.read().await;
        core_locked.payload.clone()
    }

    pub async fn get_category(&self) -> String {
        let core_locked = self.core.read().await;
        core_locked.category.clone()
    }

    pub async fn get_component_name(&self) -> String {
        let core_locked = self.core.read().await;
        core_locked.component_name.clone()
    }

    pub async fn get_owner_buffer_uid(&self) -> Option<String> {
        let core_locked = self.core.read().await;
        core_locked.owner_buffer_uid.clone()
    }

    pub async fn get_links(&self) -> HashMap<String, Vec<String>> {
        let core_locked = self.core.read().await;
        core_locked.links.link_map.clone()
    }

    ///////////////////////////////////////////
    // Core Setters
    //
    // Need to:
    // Lock Core
    // Check if committed
    // if not -> modify & drop lock
    // Announce Change
    ///////////////////////////////////////////

    pub async fn set_payload(&self, new: serde_json::Value) -> VoidOrAsyncError {
        let mut core_locked = self.core.write().await;
        if core_locked.is_committed {
            Err(Box::new(IUCoreError::ValueChangeForCommittedIU))
        } else {
            core_locked.payload = new;
            drop(core_locked);
            self.announce_change_over_backend().await
        }
    }

    /// adds a target to a link. Target should be an id. If the link doesn't exist, will be created.
    pub async fn add_target_to_link(
        &self,
        link_name: &str,
        target: impl Into<String>,
    ) -> VoidOrAsyncError {
        let mut core_locked = self.core.write().await;
        if core_locked.is_committed {
            Err(Box::new(IUCoreError::ValueChangeForCommittedIU))
        } else {
            core_locked.add_target_to_link(link_name, target);
            drop(core_locked);
            self.announce_change_over_backend().await
        }
    }

    /// Removes a target from a link. Target should be an id. If the link would have no more
    /// targets after removal, it will be removed as well.
    ///
    /// Can return respective errors, if the target or link is not found.
    pub async fn remove_target_from_link(&self, link_name: &str, target: &str) -> VoidOrAsyncError {
        let mut core_locked = self.core.write().await;
        if core_locked.is_committed {
            Err(Box::new(IUCoreError::ValueChangeForCommittedIU))
        } else {
            core_locked.remove_target_from_link(link_name, target)?;
            drop(core_locked);
            self.announce_change_over_backend().await
        }
    }

    pub async fn remove_link(&self, link_name: &str) -> VoidOrAsyncError {
        let mut core_locked = self.core.write().await;
        if core_locked.is_committed {
            Err(Box::new(IUCoreError::ValueChangeForCommittedIU))
        } else {
            core_locked.remove_link(link_name)?;
            drop(core_locked);
            self.announce_change_over_backend().await
        }
    }

    ///////////////////////////////////////////
    // Backend Stuff
    ///////////////////////////////////////////

    pub async fn announce_change_over_backend(&self) -> VoidOrAsyncError {
        let locked_core = self.core.read().await;
        let bytes = locked_core.get_bytes();
        drop(locked_core);
        self.backend
            .send_message(&self.default_channel, bytes)
            .await?;
        tokio::time::sleep(Duration::from_millis(1)).await;
        debug!("IU {} announced change.", self.uid);
        Ok(())
    }
}

impl<B: Backend + Send + Sync> Display for IU<B> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "ID: {}", self.uid)
    }
}

#[cfg(test)]
mod tests {
    use crate::backend::mqtt::MqttBackend;
    use crate::components::buffer::output::OutputBuffer;
    use crate::components::iu::IU;
    use crate::setup_test_logger;
    use log::info;
    use std::sync::atomic::{AtomicBool, Ordering};
    use std::sync::Arc;

    #[tokio::test]
    async fn update_cb_test() {
        setup_test_logger();
        let callback_processed = Arc::new(AtomicBool::new(false));
        let mut ub: OutputBuffer<MqttBackend> =
            OutputBuffer::new("ddd", "IUTest", "localhost:1883")
                .await
                .unwrap();
        let iu = IU::new(
            "whatever",
            "IUTest",
            ub.uid.clone(),
            serde_json::Value::default(),
            Arc::clone(&ub.backend),
        );
        ub.publish_iu(Arc::clone(&iu)).await.unwrap();
        let cp = Arc::clone(&callback_processed);
        iu.on_update(move |_| {
            let cbp = Arc::clone(&cp);
            Box::pin(async move {
                info!("I WAS HERE!!");
                cbp.store(true, Ordering::Relaxed);
            })
        })
        .await;
        iu.set_payload(serde_json::Value::default()).await.unwrap();
        assert!(callback_processed.load(Ordering::Relaxed))
    }
}
