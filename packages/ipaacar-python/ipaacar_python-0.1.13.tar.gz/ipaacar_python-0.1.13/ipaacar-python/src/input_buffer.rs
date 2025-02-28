use crate::iu::IU;
use crate::pyo3_asyncio;
use crate::{print_python_exception, RustIUMQTT};
use ipaacar_core::backend::mqtt::MqttBackend;
use ipaacar_core::components;
use pyo3::exceptions::PyTypeError;
use pyo3::prelude::PyAnyMethods;
use pyo3::types::{PyModule, PyType};
use pyo3::{intern, pyclass, pymethods, Bound, Py, PyAny, PyErr, Python};
use std::sync::Arc;
use tokio::sync::RwLock;

type RustMqttInputBuffer = components::buffer::input::InputBuffer<MqttBackend>;

/// IUs are objects that exist in Buffers.
/// A program can have any number of OutputBuffers and InputBuffers.
///
/// InputBuffers that components have initialized have a list of category interests,
/// set by the user.
/// Whenever an IU (or Message) of said categories is published or modified anywhere on the system,
/// the corresponding InputBuffers will receive a notification of this,
/// along with the updated IU contents.
#[pyclass(frozen)]
pub struct InputBuffer {
    pub(crate) inner: Arc<RwLock<components::buffer::input::InputBuffer<MqttBackend>>>,
}

#[pymethods]
impl InputBuffer {
    /// Async class method to create a new InputBuffer.
    ///
    /// :param uid: Can be any string that is unique for the Ipaaca Component.
    /// it is used to determine IU ownership. The means, that two output buffers with the same uid
    /// can commit an IU, if one of them is the original owner.
    /// :param component_name: refers to the ipaaca component under which the Buffer will operate.
    /// :param address: Used to connect to the backend. For a locally running MQTT Broker, the
    /// standard address would be `localhost:1883` most of the time.
    #[classmethod]
    fn new_with_connect<'p>(
        _cls: &Bound<PyType>,
        py: Python<'p>,
        uid: String,
        component_name: String,
        address: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(Self {
                inner: Arc::new(RwLock::new(
                    RustMqttInputBuffer::new(uid, component_name, address)
                        .await
                        .map_err(|e| PyTypeError::new_err(format!("{e}")))?,
                )),
            })
        })
    }

    /// returns a list of all IU uids, that the InputBuffer received so far.
    ///
    /// >>> from ipaacar.components import create_mqtt_pair
    /// >>> import asyncio
    ///
    /// >>> async def link_example():
    /// ...     i_buffer_uid = "some_input_buffer"
    /// ...     o_buffer_uid = "some_output_buffer"
    /// ...     i_b, o_b = await create_mqtt_pair(i_buffer_uid, o_buffer_uid,
    /// ...         "get_iu_ids", "localhost:1883")
    /// ...     await i_b.listen_to_category("some_category")
    /// ...     await asyncio.sleep(1) # give rust some time to finish listener setup
    /// ...     iu_1 = await o_b.create_new_iu("some_category", "{\"some\": \"json\"}")
    /// ...     iu_2 = await o_b.create_new_iu("some_category", "{\"some\": \"json\"}")
    /// ...     iu_3 = await o_b.create_new_iu("some_category", "{\"some\": \"json\"}")
    /// ...     return await i_b.get_received_iu_ids()
    ///
    /// >>> len(asyncio.run(link_example()))
    /// 3
    fn get_received_iu_ids<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let inner = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let ib = inner.read().await;
            Ok(ib.get_received_iu_ids().await)
        })
    }

    /// returns an IU by uid, if received. Throws an Error if the IU was not received.
    fn get_iu_by_id<'p>(&self, py: Python<'p>, uid: String) -> Result<Bound<'p, PyAny>, PyErr> {
        let inner = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let ib = inner.read().await;
            let rust_iu = ib
                .get_iu_by_id(&uid)
                .await
                .ok_or(PyTypeError::new_err("IU not found".to_string()))?;
            Ok(IU::create_published_from_rust_iu(rust_iu))
        })
    }

    /// A more different version of `ipaacar.components.InputBuffer.get_received_iu_ids`
    /// that returns the IUs and not just the uids.
    fn get_all_ius<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let inner = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let ib = inner.read().await;
            let rust_ius = ib.get_all_ius().await;

            Ok(rust_ius
                .into_iter()
                .map(IU::create_published_from_rust_iu)
                .collect::<Vec<_>>())
        })
    }

    /// Creates a internal listener for the category specified.
    /// The setup of the listener runs in parallel AFTER the function call. So, you will only receive
    /// IUs after the setup if finished.
    fn listen_to_category<'p>(&self, py: Python<'p>, category: String) -> Result<Bound<'p, PyAny>, PyErr> {
        let inner = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let mut ib = inner.write().await;
            ib.listen_to_category(category)
                .await
                .map_err(|e| PyTypeError::new_err(format!("{e}")))
        })
    }

    /// Add a `ipaacar.handler.IUCallbackHandlerInterface` that gets called on each NEW IU that is
    /// received.
    /// This is the main hook to handle your IUs, add additional handler on them through this.
    /// Take a look at the code examples and performance tests for correct usage.
    fn on_new_iu<'p>(&self, py: Python<'p>, callback_handler: Bound<'p, PyAny>) -> Result<Bound<'p, PyAny>, PyErr> {
        let module = PyModule::import(py, "ipaacar")?;
        let chi = module
            .getattr("handler")?
            .getattr("IUCallbackHandlerInterface")?;
        if !callback_handler.is_instance(&chi)? {
            return Err(PyTypeError::new_err(
                "Callback not an instance of IUCallbackHandlerInterface",
            ));
        };
        let inner = Arc::clone(&self.inner);
        let callback: Py<PyAny> = callback_handler.into();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let locals =
                Python::with_gil(|p| Arc::new(pyo3_asyncio::tokio::get_current_locals(p).unwrap()));
            let ib = inner.read().await;
            // let ib_uid = ib.uid.clone();
            ib.on_new_iu(move |iu: RustIUMQTT| {
                let iu = IU::create_published_from_rust_iu(iu);
                let locals = Arc::clone(&locals);
                let coroutine = Python::with_gil(|p| {
                    let chi = Py::clone_ref(&callback, p);
                    chi.call_method1(p, "process_iu_callback", (iu,)) // calling an async function returns the coroutine
                })
                    .unwrap();
                // let ib_uid = ib_uid.clone();
                Box::pin(async move {
                    let cor = Python::with_gil(|p| {
                        pyo3_asyncio::into_future_with_locals(&locals, coroutine.into_bound(p))
                            .unwrap()
                    });
                    if let Err(e) = cor.await {
                        print_python_exception(e)
                        // let err_msg = generate_python_exception_string(e);
                        // error!("executing on_new_iu callback for InputBuffer {ib_uid} failed:\n{err_msg}");
                    }
                })
            })
                .await;
            Ok(())
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
    /// Usage of this is equivalent to `ipaacar.components.InputBuffer.on_new_iu`, just with the
    /// `ipaacar.handler.MessageCallbackHandlerInterface`.
    /// The callback will be called on each message received, since they are not persistent.
    fn on_new_message<'p>(
        &self,
        py: Python<'p>,
        callback_handler: &Bound<'p, PyAny>,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        let module = PyModule::import(py, "ipaacar")?;
        let chi = module
            .getattr("handler")?
            .getattr("MessageCallbackHandlerInterface")?;
        if !callback_handler.is_instance(&chi)? {
            return Err(PyTypeError::new_err(
                "Callback not an instance of IUCallbackHandlerInterface",
            ));
        };
        let inner = Arc::clone(&self.inner);
        let callback = callback_handler.clone().unbind();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let locals =
                Python::with_gil(|p| Arc::new(pyo3_asyncio::tokio::get_current_locals(p).unwrap()));
            let ib = inner.read().await;
            // let ib_uid = ib.uid.clone();
            ib.on_new_message(move |msg: String| {
                let locals = Arc::clone(&locals);
                let coroutine = Python::with_gil(|p| {
                    callback
                        .call_method1(p, // calling an async function returns the coroutine
                                      intern!(p, "process_message_callback"),
                                      (msg,),
                        ).unwrap()
                });
                // let ib_uid = ib_uid.clone();
                Box::pin(async move {
                    let cor = Python::with_gil(|p| {
                        let cor_bind = coroutine.into_bound(p);
                        pyo3_asyncio::into_future_with_locals(&locals, cor_bind)
                            .unwrap()
                    });
                    if let Err(e) = cor.await {
                        print_python_exception(e);
                        // let err_msg = generate_python_exception_string(e);
                        // error!("executing on_new_message callback for InputBuffer {ib_uid} failed:\n{err_msg}");
                    }
                })
            })
                .await;
            Ok(())
        })
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test() {}
}
