use crate::{print_python_exception, RustIUMQTT};
use ipaacar_core::components;
use pyo3::exceptions::{PyNotImplementedError, PyTypeError};
use pyo3::prelude::{PyAnyMethods, PyModule};
use pyo3::{pyclass, pymethods, Bound, Py, PyAny, PyErr, PyResult, Python};
use std::sync::Arc;
use tokio::sync::RwLock;
use uuid::Uuid;
use crate::pyo3_asyncio;

pub(crate) enum IUVariant {
    PublishedMqtt(RustIUMQTT),
    Unpublished(components::iu::core::IUCore),
}

/// The basic unit of information transmitted (shared) in the ipaaca system is the Incremental Unit (IU),
/// based on the "General, abstract model of incremental dialogue processing" by Schlangen et al.
///
/// An IU is an object characterized by the following basic attributes:
/// * uid - a globally unique identifier
/// * category - a string representing the broad category of data, e.g. "asrresults" for transmitting the results of ASR
/// * owner - the buffer name (see below) that initially produced this IU
/// * committed - a flag that specifies whether the owner is committed to this IU and its contents (that it will remain valid and is final)
/// * payload - the IU payload: a map of string→JSON object representation, free to use by the application (see below)
/// * links - a map of string→string, representing the links of the IU (see below)
///
/// The structure looks something like that:
/// ```markdown
/// IU
/// category: myCategory
/// uid: c4f74af9-ac0f-44d6-9b04-b9294930f9bb
/// owner_buffer_uid: f19f8ef1-97fb-4be0-b7fa-3da94bc25aee
/// links: {"grounded-in": ['e2a40dc0-6337-4521-ba15-0e320116910f'] }
/// payload: {
///             "state": "DONE",
///             "resultList": [12, 24, 36, 48, 60],
///          }
/// ```
/// Refer to 'IU' and 'CoreIU' in the Rust documentation for implementation details.
#[pyclass(frozen)]
pub struct IU {
    pub(crate) inner: Arc<RwLock<IUVariant>>,
}

// rust only methods in this impl block
impl IU {
    pub fn create_published_from_rust_iu(iu: RustIUMQTT) -> Self {
        Self {
            inner: Arc::new(RwLock::new(IUVariant::PublishedMqtt(iu))),
        }
    }
}

#[pymethods]
impl IU {
    /// Creates a new, unpublished IU.
    /// The Category defines the message Type. Input Buffers listen to defined categories.
    ///
    /// ```python
    /// from ipaacar.components import IU
    ///
    /// iu = IU("my_category", "some_component_same_as_in_buffer", "{\"valid\":\"json\"}")
    /// ```
    #[new]
    fn new(category: String, component_name: String, payload: String) -> PyResult<Self> {
        let payload =
            serde_json::from_str(&payload).map_err(|e| PyTypeError::new_err(e.to_string()))?;
        let uid = Uuid::new_v4().to_string();
        let inner = components::iu::core::IUCore::new(category, component_name, None, payload, uid);
        Ok(IU {
            inner: Arc::new(RwLock::new(IUVariant::Unpublished(inner))),
        })
    }

    ///////////////////////////////////
    // Getters
    ///////////////////////////////////

    /// Returns a copy of the IU Category.
    ///
    /// >>> from ipaacar.components import IU
    /// >>> import asyncio
    ///
    /// >>> async def category_example():
    /// ...     iu = IU("this_is_my_category", "i_belong_to_this_component", "{\"some\": \"json\"}")
    /// ...     return await iu.get_category()
    ///
    /// >>> asyncio.run(category_example())
    /// 'this_is_my_category'
    fn get_category<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_category().await,
                IUVariant::Unpublished(core) => core.category.clone(),
            })
        })
    }

    /// Returns a copy of the IU uid. IU uids are randomly generated v4 uuids.
    ///
    /// >>> from ipaacar.components import IU
    /// >>> import asyncio
    ///
    /// >>> async def uid_example():
    /// ...     iu = IU("this_is_my_category", "i_belong_to_this_component", "{\"some\": \"json\"}")
    /// ...     return await iu.get_uid()
    ///
    /// >>> uid = asyncio.run(uid_example())
    /// >>> len(uid) == 36 # random v4 uuid
    /// True
    fn get_uid<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_uid().await.to_string(),
                IUVariant::Unpublished(core) => core.uid.to_string(),
            })
        })
    }

    /// Returns the Buffer, that owns the IU. If the IU is not associated with a buffer, this will
    /// return None.
    ///
    /// >>> from ipaacar.components import OutputBuffer
    /// >>> import asyncio
    ///
    /// >>> async def owner_buffer_uid_example():
    /// ...     buffer_uid = "abcde"
    /// ...     buffer = await OutputBuffer.new_with_connect(buffer_uid, "example_component", "localhost:1883")
    /// ...     iu = await buffer.create_new_iu("some_category", "{\"some\": \"json\"}")
    /// ...     return await iu.get_owner_buffer_uid()
    ///
    /// >>> asyncio.run(owner_buffer_uid_example())
    /// 'abcde'
    fn get_owner_buffer_uid<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_owner_buffer_uid().await,
                IUVariant::Unpublished(core) => core.owner_buffer_uid.clone(),
            })
        })
    }

    /// Return if a IU is committed by the owner, or not.
    /// See `ipaacar.components.OutputBuffer.commit_iu` for more details.
    fn is_committed<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.is_committed().await,
                IUVariant::Unpublished(core) => core.is_committed,
            })
        })
    }

    /// Returns the IU Payload as a String.
    /// Internally, the Payload is a encoded JSON object.
    /// You can always assume, that the String returned by this method is valid JSON (but no more).
    fn get_payload<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_payload().await.to_string(),
                IUVariant::Unpublished(core) => core.payload.to_string(),
            })
        })
    }

    /// Returns the component name of the IU. The name is set either when manually creating an IU,
    /// or by the OutputBuffer, if you use `ipaacar.components.OutputBuffer.create_new_iu`.
    /// This value cannot (and should not) be changed.
    fn get_component_name<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_component_name().await,
                IUVariant::Unpublished(core) => core.component_name.clone(),
            })
        })
    }

    /// This method returns the links as a dict where the keys are strings and the value is a
    /// list of strings. This can be used to establish dependencies between different IUs.
    /// The Key here is considered to be the "Link", while the keys are the list of "targets".
    ///
    /// See `ipaacar.components.IU.add_target_to_link` for an example.
    fn get_links<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            Ok(match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => iu.get_links().await,
                IUVariant::Unpublished(core) => core.links.link_map.clone(),
            })
        })
    }

    ///////////////////////////////////
    // Setters
    ///////////////////////////////////

    /// Set the payload for the IU. Will trigger an update announcement over the Backend,
    /// if already published.
    /// This also overwrites the entire Payload. The payload value needs to be a string that
    /// represents a valid json, otherwise this function will throw an error.
    fn set_payload<'p>(&self, py: Python<'p>, payload: String) -> Result<Bound<'p, PyAny>, PyErr> {
        let payload =
            serde_json::from_str(&payload).map_err(|e| PyTypeError::new_err(e.to_string()))?;
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match &mut *iu_arc.write().await {
                IUVariant::PublishedMqtt(iu) => iu
                    .set_payload(payload)
                    .await
                    .map_err(|e| PyTypeError::new_err(e.to_string())),
                IUVariant::Unpublished(core) => {
                    core.payload = payload;
                    Ok(())
                }
            }
        })
    }

    /// This method add a new target to a defined link. If the link is not present,
    /// it will be created. Otherwise, the function will just append the new target.
    /// The link object has this structure:
    ///
    /// ```javascript
    /// {"link_name_1":
    ///     ["target_1", "target_2"],
    ///  "link_name_2":
    ///     ["target_1", ...],
    ///  ...
    /// }
    /// ```
    ///
    /// The link/target names do not follow a convention and are fully customizable,
    /// they should however be used to describe relations between IUs.
    ///
    /// >>> from ipaacar.components import OutputBuffer
    /// >>> import asyncio
    ///
    /// >>> async def link_example():
    /// ...     buffer_uid = "some_buffer"
    /// ...     buffer = await OutputBuffer.new_with_connect(buffer_uid,
    /// ...         "example_component", "localhost:1883")
    /// ...     iu = await buffer.create_new_iu("some_category", "{\"some\": \"json\"}")
    /// ...     # since all of these methods set a write lock on the IU,
    /// ...     # gathering them makes no sense
    /// ...     await iu.add_target_to_link("some_link", "target_value_1")
    /// ...     await iu.add_target_to_link("some_link", "target_value_2")
    /// ...     await iu.add_target_to_link("another_link", "another_value")
    /// ...     await iu.remove_target_from_link("some_link", "target_value_1")
    /// ...     return await iu.get_links()
    ///
    /// >>> links = asyncio.run(link_example())
    /// >>> links["some_link"]
    /// ['target_value_2']
    /// >>> links["another_link"]
    /// ['another_value']
    fn add_target_to_link<'p>(
        &self,
        py: Python<'p>,
        link_name: String,
        target: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match &mut *iu_arc.write().await {
                IUVariant::PublishedMqtt(iu) => iu
                    .add_target_to_link(&link_name, target)
                    .await
                    .map_err(|e| PyTypeError::new_err(e.to_string())),
                IUVariant::Unpublished(core) => {
                    core.add_target_to_link(&link_name, target);
                    Ok(())
                }
            }
        })
    }

    /// Remove a the specified target for the specified link.
    /// If the target was the last one for the link,
    /// the link will be removed as well.
    /// Throws an error if either the link or the target on the link does not exist.
    fn remove_target_from_link<'p>(
        &self,
        py: Python<'p>,
        link_name: String,
        target: String,
    ) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match &mut *iu_arc.write().await {
                IUVariant::PublishedMqtt(iu) => iu
                    .remove_target_from_link(&link_name, &target)
                    .await
                    .map_err(|e| PyTypeError::new_err(e.to_string())),
                IUVariant::Unpublished(core) => {
                    core.remove_target_from_link(&link_name, &target)
                        .map_err(|e| PyTypeError::new_err(e.to_string()))?;
                    Ok(())
                }
            }
        })
    }

    /// Removes the entire link with all targets.
    /// Throws an Error if the link does not exist.
    fn remove_link<'p>(&self, py: Python<'p>, link_name: String) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match &mut *iu_arc.write().await {
                IUVariant::PublishedMqtt(iu) => iu
                    .remove_link(&link_name)
                    .await
                    .map_err(|e| PyTypeError::new_err(e.to_string())),
                IUVariant::Unpublished(core) => {
                    core.remove_link(&link_name)
                        .map_err(|e| PyTypeError::new_err(e.to_string()))?;
                    Ok(())
                }
            }
        })
    }

    /// Adds a callback that will be executed, once the IU is updated.
    /// The callback doesn't differentiate between local or remote updates.
    ///
    /// Take a look at
    /// `ipaacar.handler.IUCallbackHandlerInterface`
    /// for more details and examples.
    fn add_callback<'p>(&self, py: Python<'p>, callback: &Bound<'p, PyAny>) -> Result<Bound<'p, PyAny>, PyErr> {
        let module = PyModule::import(py, "ipaacar")?;
        let chi = module
            .getattr("handler")?
            .getattr("IUCallbackHandlerInterface")?;
        if !callback.is_instance(&chi)? {
            return Err(PyTypeError::new_err(
                "Callback not an instance of CallbackHandlerInterface",
            ));
        };
        let callback = callback.clone().unbind();
        let iu_arc = Arc::clone(&self.inner);

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let iu = match &*iu_arc.read().await {
                IUVariant::PublishedMqtt(iu) => Arc::clone(iu),
                IUVariant::Unpublished(_) => {
                    return Err(PyNotImplementedError::new_err(
                        "Adding callbacks for unpublished ius not yet implemented.",
                    ));
                }
            };

            let locals = Python::with_gil(|p| {
                // run callback on event loop that awaited add_callback
                Arc::new(pyo3_asyncio::tokio::get_current_locals(p).unwrap())
            });

            // let callback = Py::clone_ref(&callback, p);
            // let iu_id = iu.get_uid().await.to_string();
            iu.on_update(move |iu: RustIUMQTT| {
                let locals = Arc::clone(&locals);
                let iu = IU::create_published_from_rust_iu(iu);
                let coroutine = Python::with_gil(|p| {
                    let chi = Py::clone_ref(&callback, p);
                    chi.call_method1(p, "process_iu_callback", (iu,)) // calling an async function returns the coroutine
                })
                    .unwrap();
                // let iu_id = iu_id.clone();
                Box::pin(async move {
                    let cor = Python::with_gil(|p| {
                        pyo3_asyncio::into_future_with_locals(&locals, coroutine.into_bound(p))
                            .unwrap()
                    });
                    if let Err(e) = cor.await {
                        print_python_exception(e);
                        // let err_msg = generate_python_exception_string(e);
                        // error!("executing on_update callback for IU {iu_id} failed:\n{err_msg}");
                    }
                })
            })
                .await;

            Ok(())
        })
    }

    /// This will trigger a change signal over the backend,
    /// without changing anything about the IU. This is useful,
    /// if you want to manually trigger callbacks on the IU.
    fn announce_change_over_backend<'p>(&self, py: Python<'p>) -> Result<Bound<'p, PyAny>, PyErr> {
        let iu_arc = Arc::clone(&self.inner);
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match &mut *iu_arc.write().await {
                IUVariant::PublishedMqtt(iu) => iu
                    .announce_change_over_backend()
                    .await
                    .map_err(|e| PyTypeError::new_err(e.to_string())),
                IUVariant::Unpublished(_) => Ok(()),
            }
        })
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test() {}
}
