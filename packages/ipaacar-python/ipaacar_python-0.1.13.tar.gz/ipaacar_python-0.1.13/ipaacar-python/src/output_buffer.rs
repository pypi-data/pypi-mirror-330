use crate::iu::{IUVariant, IU};
use ipaacar_core::backend::mqtt::MqttBackend;
use ipaacar_core::components;
use log::error;
use pyo3::exceptions::PyTypeError;
use pyo3::types::PyType;
use pyo3::{pyclass, pymethods, Bound, PyAny, PyErr, Python};
use std::mem;
use std::sync::Arc;
use tokio::sync::RwLock;
use crate::pyo3_asyncio;

type RustMqttOutputBuffer = components::buffer::output::OutputBuffer<MqttBackend>;

/// IUs are objects that exist in Buffers.
/// A program can have any number of OutputBuffers and InputBuffers.
/// When a new IU has been created, it has to be placed in an OutputBuffer.
/// It is thereby published.
#[pyclass(frozen)]
pub struct OutputBuffer {
    pub(crate) inner: Arc<RwLock<RustMqttOutputBuffer>>,
}

#[pymethods]
impl OutputBuffer {
    /// Async class method to create a new OutputBuffer.
    ///
    /// :param uid: Can be any string that is unique for the Ipaaca Component.
    /// it is used to determine IU ownership. The means, that two output buffers with the same uid
    /// can commit an IU, if one of them is the original owner.
    /// :param component_name: refers to the ipaaca component under which the Buffer will operate.
    /// :param address: Used to connect to the backend. For a locally running MQTT Broker, the
    /// standard address would be `localhost:1883` most of the time.
    #[classmethod]
    fn new_with_connect<'p>(
        _cls: &Bound<'_, PyType>,
        py: Python<'p>,
        uid: String,
        component_name: String,
        address: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(Self {
                inner: Arc::new(RwLock::new(
                    RustMqttOutputBuffer::new(uid, component_name, address)
                        .await
                        .map_err(|e| PyTypeError::new_err(format!("{e}")))?,
                )),
            })
        })
    }

    /// Convenience function to create an IU, set the correct identifiers and immediately publish it.
    fn create_new_iu<'p>(
        &self,
        py: Python<'p>,
        category: String,
        payload: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        let inner = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let mut ob = inner.write().await;
            let iu = ob
                .create_new_iu(
                    category,
                    serde_json::from_str(&payload)
                        .map_err(|e| PyTypeError::new_err(format!("{e}")))?,
                    true,
                )
                .await
                .map_err(|e| PyTypeError::new_err(format!("{e}")))?;
            Ok(IU::create_published_from_rust_iu(iu))
        })
    }

    /// Publish an IU on this OutputBuffer, that is not assigned to a buffer yet.
    fn publish_iu<'p>(&self, py: Python<'p>, iu: &IU) -> Result<Bound<'p, PyAny>, PyErr> {
        let buffer_arc = Arc::clone(&self.inner);
        let iu_arc = Arc::clone(&iu.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let mut iu = iu_arc.write().await;
            let mut new_variant = match &mut *iu {
                IUVariant::PublishedMqtt(var) => {
                    error!("Tried to publish already published iu");
                    IUVariant::PublishedMqtt(Arc::clone(var))
                }
                IUVariant::Unpublished(core) => {
                    let buf = buffer_arc.read().await;
                    let (backend, uid) = (Arc::clone(&buf.backend), buf.uid.clone());
                    drop(buf);
                    let new_inner = components::iu::IU::from_core(core.clone(), Some(uid), backend);
                    buffer_arc
                        .write()
                        .await
                        .publish_iu(Arc::clone(&new_inner))
                        .await
                        .map_err(|e| PyTypeError::new_err(format!("{e}")))
                        .unwrap();
                    IUVariant::PublishedMqtt(new_inner)
                }
            };
            mem::swap(&mut new_variant, &mut iu);
            Ok(())
        })
    }

    /// This method commits the IU. The buffer needs to be the owner of the IU.
    /// The IU cannot be changed after it is committed.
    /// For simplicity reasons, this is only checked when sending changes, not when receiving them.
    /// See `ipaacar.components.IU.get_owner_buffer_uid`.
    fn commit_iu<'p>(&self, py: Python<'p>, iu: &IU) -> Result<Bound<'p, PyAny>, PyErr> {
        let buffer_arc = Arc::clone(&self.inner);
        let iu_arc = Arc::clone(&iu.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let buf = buffer_arc.read().await;
            let buffer_id = buf.uid.clone();
            let mut iu = iu_arc.write().await;
            match &mut *iu {
                IUVariant::PublishedMqtt(p_iu) => p_iu
                    .commit(&buffer_id)
                    .await
                    .map_err(|e| PyTypeError::new_err(format!("{e}"))),
                IUVariant::Unpublished(core) => core
                    .commit(&buffer_id)
                    .await
                    .map_err(|e| PyTypeError::new_err(format!("{e}"))),
            }
        })
    }

    /// The Message is a special case of an IU:
    /// it is a non-persistent read-only version of the IU.
    /// It can be used whenever you just want to send current information
    /// (akin to lightweight message-passing systems, hence the name),
    /// without the possibility of later modification.
    /// The benefit is that Messages are only present for the time of reception
    /// and do not occupy additional cumulative resources.
    ///
    /// Sends a message to this category. See `ipaacar.components.InputBuffer.on_new_message`
    /// for more a example.
    fn send_message<'p>(
        &self,
        py: Python<'p>,
        category: String,
        message: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        let buffer_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let ob = buffer_arc.read().await;
            ob.send_message(&category, message)
                .await
                .map_err(|e| PyTypeError::new_err(format!("{e}")))
        })
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test() {}
}
