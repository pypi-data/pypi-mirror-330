use std::collections::HashMap;
use std::error::Error;
use std::future::Future;
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;
use bytes::Bytes;
use log::{error, info};
use poster::prelude::StreamExt;
use poster::{ConnectOpts, Context, ContextHandle, PublishOpts, SubscribeOpts, SubscriptionOpts};
use thiserror::Error;
use tokio::net::tcp::{OwnedReadHalf, OwnedWriteHalf};
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio::task::JoinHandle;
use tokio::time;
use tokio_util::compat::{Compat, TokioAsyncReadCompatExt, TokioAsyncWriteCompatExt};

use crate::backend::Backend;
use crate::VoidOrAsyncError;

type ContextCompat = Context<Compat<OwnedReadHalf>, Compat<OwnedWriteHalf>>;

/// Basic struct that handles Mqtt operations.
/// Sets up a task that occasionally pings the broker
pub struct MqttBackend {
    handle: Arc<Mutex<ContextHandle>>,
    client_context: Option<ContextCompat>,
    subscriptions: Mutex<HashMap<String, JoinHandle<VoidOrAsyncError>>>,
}

impl MqttBackend {
    // necessary for NanoMQ, client gets disconnected otherwise
    async fn register_broker_ping(&self) {
        let handle = Arc::clone(&self.handle);
        tokio::spawn(async move {
            loop {
                let mut h = handle.lock().await;
                h.ping().await.unwrap_or_else(|_| {
                    error!("Ping to Broker Failed");
                });
                drop(h);
                time::sleep(Duration::from_secs(5)).await;
            }
        });
    }
}

#[async_trait]
impl Backend for MqttBackend {
    async fn new() -> Self {
        let (ctx, handle) = Context::new();
        Self {
            handle: Arc::new(Mutex::new(handle)),
            client_context: Some(ctx),
            subscriptions: Mutex::new(HashMap::new()),
        }
    }

    async fn connect(&mut self, address: impl Into<String> + Send) -> VoidOrAsyncError {
        let address = address.into();
        let ctx = self.client_context.take();
        let ctx_task = tokio::spawn(async move {
            let (rx, tx) = TcpStream::connect(address).await?.into_split();
            let mut ctx = ctx.expect("Setting up connection failed. Couldn't unpack context.");
            ctx.set_up((rx.compat(), tx.compat_write()))
                .connect(ConnectOpts::default())
                .await?;
            if let Err(err) = ctx.run().await {
                panic!("\"{}\", exiting...", err);
            } else {
                info!("[context] Context exited.");
            }
            Ok::<(), Box<dyn Error + Send + Sync>>(())
        });

        tokio::spawn(async {
            if let Err(e) = ctx_task.await? {
                error!("{}", e)
            }
            Ok::<(), Box<dyn Error + Send + Sync>>(())
        });
        self.register_broker_ping().await;
        Ok(())
    }

    async fn send_message(
        &self,
        channel: &str,
        message: impl Into<Bytes> + Send,
    ) -> VoidOrAsyncError {
        let message = message.into();
        let opts = PublishOpts::default().topic_name(channel).payload(&message);
        let mut h = self.handle.lock().await;
        h.publish(opts).await?;
        drop(h);
        Ok(())
    }

    async fn add_callback<F>(
        &self,
        channel_id: impl Into<String> + Send,
        callback_id: impl Into<String> + Send,
        callback: (impl Fn(Vec<u8>) -> F + Send + Sync + 'static),
    ) -> VoidOrAsyncError
    where
        F: Future<Output = ()> + Send + 'static,
    {
        let channel_id = channel_id.into();
        let callback_id = callback_id.into();
        let call_id = callback_id.clone();
        let handle_mut = Arc::clone(&self.handle);
        let join_handle = tokio::spawn(async move {
            let opts =
                SubscribeOpts::default().subscription(&channel_id, SubscriptionOpts::default());
            let mut handle = handle_mut.lock().await;
            let subscription = handle.subscribe(opts).await?;
            drop(handle);
            let mut subscription = subscription.stream();
            while let Some(msg) = subscription.next().await {
                callback(Vec::from(msg.payload())).await; // need to clone since i cant acquire ownership
            }
            Ok(())
        });
        let mut subs = self.subscriptions.lock().await;
        if subs.contains_key(&callback_id) {
            Err(Box::new(CallbackError::AddCallbackFailed))
        } else {
            subs.insert(call_id, join_handle);
            Ok(())
        }
    }

    async fn remove_callback(&self, id: &str) -> VoidOrAsyncError {
        let mut subs = self.subscriptions.lock().await;
        let ret = subs.remove(id);
        match ret {
            Some(join) => {
                join.abort();
                Ok(())
            }
            None => Err(Box::new(CallbackError::RemoveCallbackFailed)),
        }
    }
}

#[derive(Error, Debug)]
pub enum CallbackError {
    #[error("Couldn't add Callback")]
    AddCallbackFailed,
    #[error("Couldn't remove Callback")]
    RemoveCallbackFailed,
}
