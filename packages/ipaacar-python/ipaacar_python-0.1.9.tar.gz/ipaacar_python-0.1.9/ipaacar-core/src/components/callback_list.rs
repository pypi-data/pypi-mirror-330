use crate::{Callback, CallbackFuture};

/// struct that handles Callback storing and calling when new data is received.
pub struct CallbackList<T> {
    list: Vec<Box<Callback<T>>>,
}

impl<T> CallbackList<T> {
    pub fn new() -> Self {
        Self { list: Vec::new() }
    }

    /// store new callbacks
    pub fn push<F>(&mut self, f: F)
    where
        F: Fn(T) -> CallbackFuture<()>,
        F: Send + Sync + 'static,
    {
        self.list.push(Box::new(f))
    }

    /// calls all callbacks by spawning coroutines with the data
    pub async fn call(&self, t: T)
    where
        T: Clone,
    {
        for f in &self.list {
            // spawns each callback separately, so they *might* run in parallel.
            tokio::spawn(f(t.clone()));
        }
    }
}

#[cfg(test)]
mod tests {
    use log::info;
    use std::sync::atomic::{AtomicI32, Ordering};
    use std::sync::Arc;
    use std::time::Duration;

    use crate::components::callback_list::CallbackList;
    use crate::setup_test_logger;

    #[tokio::test]
    async fn test() {
        setup_test_logger();
        let y = Arc::new(AtomicI32::new(5));
        let mut calls = CallbackList::new();
        calls.push(|i| {
            // just to show that move works as well
            Box::pin(async move {
                info!("I print i: {i}");
            })
        });
        calls.push(|i| {
            Box::pin(async move {
                info!("I print i as well: {}", i);
            })
        });
        let y_2 = Arc::clone(&y);
        calls.push(move |i| {
            let y = Arc::clone(&y_2);
            Box::pin(async move {
                info!(
                    "I move into the closure! i + y: {}",
                    i + y.load(Ordering::Relaxed)
                );
            })
        });
        let handle = tokio::spawn(async move {
            calls.call(34).await;
        });

        handle.await.unwrap();
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}
