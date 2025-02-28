use crate::backend::Backend;
use crate::components::buffer::input::InputBuffer;
use crate::components::buffer::output::OutputBuffer;
use std::error::Error;

pub(crate) mod buffer_iu_cb_manager;
pub mod input;
pub mod output;

/// Creates an Input-/OutputBuffer pair. Both of them will belong to the same component but still
/// use separate Backend connections.
pub async fn create_pair<B: Backend + Send + Sync + 'static>(
    input_uid: impl Into<String> + Send,
    output_uid: impl Into<String> + Send,
    component_name: impl Into<String> + Send + Clone,
    address: impl Into<String> + Send + Clone,
) -> Result<(InputBuffer<B>, OutputBuffer<B>), Box<dyn Error + Sync + Send>> {
    let ib = InputBuffer::new(input_uid, component_name.clone(), address.clone()).await?;
    let ob = OutputBuffer::new(output_uid, component_name, address).await?;
    Ok((ib, ob))
}
