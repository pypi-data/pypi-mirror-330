use std::error::Error;
use std::future::Future;
use std::pin::Pin;

#[cfg(test)]
use log::LevelFilter;

pub mod backend;
pub mod components;

type VoidOrAsyncError = Result<(), Box<dyn Error + Send + Sync>>;
pub type CallbackFuture<O> = Pin<Box<dyn Future<Output = O> + Send>>;
/// callbacks processed by Ipaacar need to implement these traits.
/// Wrap your async functions/closures accordingly
/// (e.g. with Box::pin) when you implement a new wrapper.
/// This can be simplified once async closures with arguments are stabilized.
pub type Callback<T> = dyn (Fn(T) -> CallbackFuture<()>) + Send + Sync;

#[cfg(test)]
fn setup_test_logger() {
    let _ = env_logger::builder()
        .filter_level(LevelFilter::Debug)
        .is_test(true)
        .try_init();
}
