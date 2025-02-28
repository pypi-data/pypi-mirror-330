use pyo3::exceptions::PyTypeError;
use std::sync::Arc;

use pyo3::prelude::*;
use tokio::sync::RwLock;

use ipaacar_core::backend::mqtt::MqttBackend;
use ipaacar_core::components::buffer;

use crate::input_buffer::InputBuffer;
use crate::iu::IU;
use crate::output_buffer::OutputBuffer;
use pyo3_async_runtimes as pyo3_asyncio; // https://github.com/awestlake87/pyo3-asyncio/issues/119

pub mod input_buffer;
pub mod iu;
pub mod output_buffer;

type RustIUMQTT = Arc<ipaacar_core::components::iu::IU<MqttBackend>>;

/// Convenience function to create an Input- and OutputBuffer on the same address.
/// Requires the use of a Mqtt Backend.
#[pyfunction]
fn create_mqtt_pair(
    py: Python,
    input_uid: String,
    output_uid: String,
    component_name: String,
    address: String,
) -> Result<Bound<PyAny>, PyErr> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let (ib, ob) =
            buffer::create_pair::<MqttBackend>(input_uid, output_uid, component_name, address)
                .await
                .map_err(|e| PyTypeError::new_err(format!("{e}")))?;
        Ok((
            InputBuffer {
                inner: Arc::new(RwLock::new(ib)),
            },
            OutputBuffer {
                inner: Arc::new(RwLock::new(ob)),
            },
        ))
    })
}

/// This submodule contains the essential Ipaaca Components.
/// Also keep in mind that this is just a wrapper around functionality that is implemented in Rust.
/// If you have want to extend the functionality of this module, consider doing this directly for the core Rust
/// library.
///
/// The core Rust library also supports logging on various levels.
/// * error
///     * Callback triggered on an IU, that doesn't exist anymore
///     * Invalid IU update received
///     * Can't ping broker (Mqtt)
///     * Tried to publish already published IU
///     * Couldn't add IU update listener
///     * Context exited (Disconnected by MqttBackend)
///     * Message with invalid encoding received
///     * Couldn't listen to category on InputBuffer
/// * info
///     * New IU received in InputBuffer
///     * New IU placed in OutputBuffer
///     * Context Exited (Disconnected by MqttClient)
///     * New Buffer established connection to Backend
///     * InputBuffer listening to new category for IUs/Messages
/// * debug
///     * InputBuffer detected possible new IU
///     * IU updated
///     * IU announced changed over Backend
///
/// The Rust logger is always registered for the Python bindings.
/// In order to print the logs to the console, you can do something like ths:
///
/// >>> import logging
/// >>> import sys
/// >>> import ipaacar
/// >>> import asyncio
///
/// >>> logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
/// >>> asyncio.run(ipaacar.components.OutputBuffer.new_with_connect(
/// ...     "abc", "def", "localhost:1883"))
/// FO:ipaacar_core.components.buffer.output:new OutputBuffer abc connected to localhost:1883
///
/// For more information on how to properly use logging in Python,
/// check out the [docs](https://docs.python.org/3/howto/logging.html).
///
#[pymodule]
fn components(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    // this connects the rust logger to python logging
    pyo3_log::init();

    m.add_class::<IU>()?;
    m.add_class::<InputBuffer>()?;
    m.add_class::<OutputBuffer>()?;
    m.add_function(wrap_pyfunction!(create_mqtt_pair, m)?)?;
    Ok(())
}

// fn generate_python_exception_string(e: PyErr) -> String {
//     Python::with_gil(|p| {
//         let traceback = e.traceback_bound(p);
//         if traceback.is_none() {
//             return format!("no traceback available.\nException:\n{e}");
//         }
//         let traceback_formatted = traceback.unwrap().format();
//         match traceback_formatted {
//             Ok(t) => { t }
//             Err(te) => {
//                 format!("traceback available but formatting failed: {te}.\nException:\n{e}")
//             }
//         }
//     })
// }

fn print_python_exception(e: PyErr) {
    Python::with_gil(|p| {
        e.print_and_set_sys_last_vars(p);
    });
}