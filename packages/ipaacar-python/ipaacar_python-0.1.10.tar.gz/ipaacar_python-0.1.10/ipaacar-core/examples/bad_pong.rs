use ipaacar_core::backend::mqtt::MqttBackend;
use ipaacar_core::components::buffer::create_pair;
use serde_json::json;
use std::sync::Arc;
use std::time::Duration;

#[tokio::main]
async fn main() {
    env_logger::init();
    let (mut ib, _ob) =
        create_pair::<MqttBackend>("ibpong", "obpong", "PingPong", "localhost:1883")
            .await
            .unwrap();
    ib.on_new_iu(|new_iu| {
        let new_iu_copy = Arc::clone(&new_iu);
        Box::pin(async move {
            let iu = Arc::clone(&new_iu_copy);
            iu.on_update(|iu| {
                let iu_copy = Arc::clone(&iu);
                Box::pin(async move {
                    let iu = Arc::clone(&iu_copy);
                    let mut payload = iu.get_payload().await;
                    let count = payload.get("C").unwrap().as_u64().unwrap();
                    println!("PONG, {count}");
                    payload["C"] = json!(count + 1);
                    match iu.set_payload(payload).await {
                        Ok(_) => {}
                        Err(_) => std::process::exit(-1),
                    };
                })
            })
            .await;
        })
    })
    .await;
    ib.listen_to_category("ping").await.unwrap();
    loop {
        tokio::time::sleep(Duration::from_secs(60)).await;
    }
}
