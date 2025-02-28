use crate::VoidOrAsyncError;
use async_trait::async_trait;
use bytes::Bytes;
use std::future::Future;

pub mod mqtt;

/// Defines the Interface between Backend and Buffer. If you want to use something other than Mqtt,
/// just implement and use this trait.
#[async_trait]
pub trait Backend {
    /// Simple constructor required. Use this to initialize vec etc Should NOT call connect.
    async fn new() -> Self;
    /// Connect to the Backend in Question. Might be sensible to just call it in the constructor
    async fn connect(&mut self, address: impl Into<String> + Send) -> VoidOrAsyncError;
    /// Sends a message to the corresponding channel.
    async fn send_message(
        &self,
        channel_id: &str,
        message: impl Into<Bytes> + Send,
    ) -> VoidOrAsyncError;
    /// creates or uses a listener to call a callback, when a message on a given channel is received
    async fn add_callback<F>(
        &self,
        channel_id: impl Into<String> + Send,
        callback_id: impl Into<String> + Send,
        callback: impl Fn(Vec<u8>) -> F + Send + Sync + 'static,
    ) -> VoidOrAsyncError
    where
        F: Future<Output = ()> + Send + 'static;
    /// removes listeners for the given channel
    async fn remove_callback(&self, callback_id: &str) -> VoidOrAsyncError;
}
