use log::{debug, error, info};
use std::collections::HashMap;
use std::error::Error;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::{Mutex, RwLock};

use uuid::Uuid;

use crate::backend::Backend;
use crate::components::async_utils::{handle_data_to_new_iu, handle_new_msg};
use crate::components::buffer::buffer_iu_cb_manager::IUCallbackManager;
use crate::components::callback_list::CallbackList;
use crate::components::iu::IU;
use crate::{CallbackFuture, VoidOrAsyncError};

/// Models the Ipaaca OutputBuffer.
/// Receives ius from OutputBuffers it listens to.
pub struct InputBuffer<B: Backend + Send + Sync> {
    pub uid: String,
    component_name: String,
    received_ius: Arc<RwLock<HashMap<String, Arc<IU<B>>>>>,
    backend: Arc<B>,
    callback_manager: Arc<Mutex<IUCallbackManager<B>>>,
    new_iu_callbacks: Arc<Mutex<CallbackList<Arc<IU<B>>>>>,
    message_callbacks: Arc<Mutex<CallbackList<String>>>,
}

impl<B: Backend + Send + Sync + 'static> InputBuffer<B> {
    pub async fn new(
        uid: impl Into<String>,
        component_name: impl Into<String> + Send + Clone,
        address: impl Into<String> + Send + Clone,
    ) -> Result<InputBuffer<B>, Box<dyn Error + Send + Sync>> {
        let uid = uid.into();
        let component_name = component_name.into();
        let mut be = B::new().await;
        be.connect(address.clone()).await?;
        let backend = Arc::new(be);
        let received_ius = Arc::new(RwLock::new(HashMap::new()));
        let callback_manager = Arc::new(Mutex::new(IUCallbackManager::new(
            Arc::clone(&backend),
            Arc::clone(&received_ius),
        )));
        let new_iu_callbacks = Arc::new(Mutex::new(CallbackList::new()));
        let message_callbacks = Arc::new(Mutex::new(CallbackList::new()));
        let buffer = Self {
            uid,
            component_name,
            received_ius,
            backend,
            callback_manager,
            new_iu_callbacks,
            message_callbacks,
        };
        info!(
            "new InputBuffer {} connected to {}",
            &buffer.uid,
            address.into()
        );
        Ok(buffer)
    }

    pub async fn get_received_iu_ids(&self) -> Vec<String> {
        let ius = self.received_ius.read().await;
        ius.keys().cloned().collect()
    }

    pub async fn get_iu_by_id(&self, uid: &str) -> Option<Arc<IU<B>>> {
        let ius = self.received_ius.read().await;
        ius.get(uid).map(Arc::clone)
    }

    pub async fn get_all_ius(&self) -> Vec<Arc<IU<B>>> {
        let ius = self.received_ius.read().await;
        ius.values().map(Arc::clone).collect()
    }

    /// listens to a category on this component
    /// the received_ius Map.
    pub async fn listen_to_category(
        &mut self,
        category: impl Into<String> + Send,
    ) -> VoidOrAsyncError {
        let category = category.into();
        let component_name = self.component_name.to_string();
        let r_ius = Arc::clone(&self.received_ius);
        let cbm = Arc::clone(&self.callback_manager);
        let backend = Arc::clone(&self.backend);
        let new_iu_callbacks = Arc::clone(&self.new_iu_callbacks);
        let iu_cb = move |data: Vec<u8>| {
            debug!("possible new IU received");
            handle_data_to_new_iu(
                data,
                component_name.clone(),
                Arc::clone(&r_ius),
                Arc::clone(&cbm),
                Arc::clone(&backend),
                Arc::clone(&new_iu_callbacks),
            )
        };
        let listen_address = format!("{}/{}/IU/#", self.component_name, &category);
        let cb_id = Uuid::new_v4();
        let handle = self
            .backend
            .add_callback(listen_address, cb_id.to_string(), iu_cb)
            .await;
        match handle {
            Ok(_) => info!(
                "Listening to category {} on Input Buffer {} for IUs",
                &category, &self.uid
            ),
            Err(e) => error!(
                "Error listening to category {} on Input Buffer {}: {}",
                &category, &self.uid, e
            ),
        }
        let msg_cbs = Arc::clone(&self.message_callbacks);
        let msg_listener = move |data: Vec<u8>| {
            let cbs = Arc::clone(&msg_cbs);
            handle_new_msg(data, cbs)
        };
        let cb_id = Uuid::new_v4();
        let handle = self
            .backend
            .add_callback(
                format!("{}/{}/M", self.component_name, category),
                cb_id.to_string(),
                msg_listener,
            )
            .await;
        match handle {
            Ok(_) => info!(
                "Listening to category {} on Input Buffer {} for messages",
                &category, &self.uid
            ),
            Err(e) => error!(
                "Error listening to category {} on Input Buffer {}: {}",
                &category, &self.uid, e
            ),
        }
        tokio::time::sleep(Duration::from_millis(1)).await;
        Ok(())
    }

    pub async fn on_new_iu<F>(&self, cb: F)
    where
        F: Fn(Arc<IU<B>>) -> CallbackFuture<()>,
        F: Send + Sync + 'static,
    {
        let mut cb_list = self.new_iu_callbacks.lock().await;
        cb_list.push(cb);
    }

    pub async fn on_new_message<F>(&self, cb: F)
    where
        F: Fn(String) -> CallbackFuture<()>,
        F: Send + Sync + 'static,
    {
        let mut cb_list = self.message_callbacks.lock().await;
        cb_list.push(cb);
    }
}

#[cfg(test)]
mod tests {
    use crate::backend::mqtt::MqttBackend;
    use crate::components::buffer::create_pair;
    use crate::components::buffer::input::InputBuffer;
    use crate::components::buffer::output::OutputBuffer;
    use crate::setup_test_logger;
    use std::sync::atomic::{AtomicBool, Ordering};
    use std::sync::Arc;
    use std::time::Duration;

    #[tokio::test]
    async fn iu_test() {
        setup_test_logger();
        let iu_received = Arc::new(AtomicBool::new(false));
        let mut ob: OutputBuffer<MqttBackend> =
            OutputBuffer::new("abc", "IBTest", "localhost:1883")
                .await
                .unwrap();
        let mut ib: InputBuffer<MqttBackend> = InputBuffer::new("def", "IBTest", "localhost:1883")
            .await
            .unwrap();
        let temp = Arc::clone(&iu_received);
        ib.on_new_iu(move |_| {
            let iur = Arc::clone(&temp);
            Box::pin(async move {
                iur.store(true, Ordering::Relaxed);
            })
        })
        .await;
        ib.listen_to_category("whatever").await.unwrap();

        let _iu = ob
            .create_new_iu("whatever", serde_json::Value::default(), true)
            .await
            .unwrap();

        tokio::time::sleep(Duration::from_secs(3)).await;
        assert!(iu_received.load(Ordering::Relaxed))
    }

    #[tokio::test]
    async fn msg_test() {
        setup_test_logger();
        let (mut ib, ob) = create_pair::<MqttBackend>(
            "ib_msg_test",
            "ob_msg_test",
            "message_test",
            "localhost:1883",
        )
        .await
        .unwrap();
        let msg_received = Arc::new(AtomicBool::new(false));
        let temp = Arc::clone(&msg_received);
        ib.on_new_message(move |_| {
            let iur = Arc::clone(&temp);
            Box::pin(async move {
                iur.store(true, Ordering::Relaxed);
            })
        })
        .await;
        ib.listen_to_category("test").await.unwrap();
        tokio::time::sleep(Duration::from_secs(1)).await;
        ob.send_message("test", "whatever").await.unwrap();
        tokio::time::sleep(Duration::from_secs(1)).await;
        assert!(msg_received.load(Ordering::Relaxed))
    }
}
