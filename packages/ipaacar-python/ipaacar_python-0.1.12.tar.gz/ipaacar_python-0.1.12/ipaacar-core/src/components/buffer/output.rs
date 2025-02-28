use crate::backend::Backend;
use crate::components::buffer::buffer_iu_cb_manager::IUCallbackManager;
use crate::components::iu::IU;
use crate::VoidOrAsyncError;
use bytes::Bytes;
use log::info;
use std::collections::HashMap;
use std::error::Error;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::RwLock;

/// OutputBuffer as described by the Ipaaca Specification.
pub struct OutputBuffer<B: Backend + Send + Sync> {
    pub uid: String,
    pub component_name: String,
    pub backend: Arc<B>,
    owned_ius: Arc<RwLock<HashMap<String, Arc<IU<B>>>>>,
    callback_manager: IUCallbackManager<B>,
}

impl<B: Backend + Send + Sync + 'static> OutputBuffer<B> {
    pub async fn new(
        uid: impl Into<String>,
        component_name: impl Into<String> + Send + Clone,
        address: impl Into<String> + Send + Clone,
    ) -> Result<OutputBuffer<B>, Box<dyn Error + Send + Sync>> {
        let uid = uid.into();
        let component_name = component_name.into();
        let mut be = B::new().await;
        be.connect(address.clone()).await?;
        let backend = Arc::new(be);
        let owned_ius = Arc::new(RwLock::new(HashMap::default()));
        let callback_manager = IUCallbackManager::new(Arc::clone(&backend), Arc::clone(&owned_ius));
        let buffer = Self {
            uid,
            component_name,
            owned_ius,
            backend,
            callback_manager,
        };
        info!(
            "new OutputBuffer {} connected to {}",
            &buffer.uid,
            address.into()
        );
        Ok(buffer)
    }

    pub async fn create_new_iu(
        &mut self,
        category: impl Into<String>,
        payload: serde_json::Value,
        publish: bool,
    ) -> Result<Arc<IU<B>>, Box<dyn Error + Send + Sync>> {
        let iu = IU::new(
            category.into(),
            &self.component_name,
            self.uid.to_string(),
            payload,
            Arc::clone(&self.backend),
        );
        if publish {
            self.publish_iu(Arc::clone(&iu)).await?;
        }
        Ok(iu)
    }

    pub async fn publish_iu(&mut self, iu: Arc<IU<B>>) -> VoidOrAsyncError {
        let uid = iu.get_uid().await;
        let mut owned_ius = self.owned_ius.write().await;
        owned_ius.insert(uid.to_string(), Arc::clone(&iu));
        drop(owned_ius);
        info!("IU {} placed in OutputBuffer {}", &uid, self.uid);
        self.callback_manager
            .add_iu_updater(&self.component_name, uid)
            .await?;
        tokio::time::sleep(Duration::from_millis(10)).await; // necessary for the coroutines to finish
        iu.announce_change_over_backend().await?;
        Ok(())
    }

    pub async fn commit_iu(&self, iu: Arc<IU<B>>) -> VoidOrAsyncError {
        iu.commit(&self.uid).await
    }

    /// send non-persistent messages to input buffers.
    /// Messages are (at the moment) not encoded.
    pub async fn send_message(
        &self,
        category: &str,
        message: impl Into<Bytes> + Send,
    ) -> VoidOrAsyncError {
        let address = format!("{}/{}/M", self.component_name, category);
        self.backend.send_message(&address, message).await
    }
}

#[cfg(test)]
mod test {
    use crate::backend::mqtt::MqttBackend;
    use crate::components::buffer::output::OutputBuffer;
    use crate::components::iu::IU;
    use crate::setup_test_logger;
    use std::sync::Arc;

    #[tokio::test]
    async fn ob_iu_test() {
        setup_test_logger();
        let mut mqtt_ob: OutputBuffer<MqttBackend> =
            OutputBuffer::new("some_uid", "OutputBufferTest", "localhost:1883")
                .await
                .unwrap();
        let payload = serde_json::Value::default();
        let iu = IU::new(
            "whatever",
            "OutputBufferTest",
            mqtt_ob.uid.to_string(),
            payload,
            Arc::clone(&mqtt_ob.backend),
        );
        let iu_2 = Arc::clone(&iu);
        mqtt_ob.publish_iu(iu).await.unwrap();
        iu_2.set_payload(serde_json::Value::default())
            .await
            .unwrap();
    }

    #[tokio::test]
    async fn msg_test() {
        setup_test_logger();
        let mqtt_ob: OutputBuffer<MqttBackend> =
            OutputBuffer::new("some_uid", "OutputBufferTest", "localhost:1883")
                .await
                .unwrap();
        mqtt_ob
            .send_message("ob_test", "u received my msg!")
            .await
            .unwrap();
    }
}
