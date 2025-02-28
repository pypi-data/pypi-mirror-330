use ipaacar_core::backend::mqtt::MqttBackend;
use ipaacar_core::components::buffer::create_pair;
use serde_json::json;
use std::sync::Arc;
use std::time::Duration;

/// Ipaacar Example
/// Run: cargo run --bin ping -q
/// from the ipaacar-core directory
#[tokio::main]
async fn main() {
    env_logger::init();
    let (mut ib, mut ob) =
        create_pair::<MqttBackend>("ibping", "obping", "PingPong", "localhost:1883")
            .await
            .unwrap();
    let payload = json!({
        "C": 0
    });
    println!("1");
    ib.listen_to_category("obpong").await.unwrap();
    println!("2");
    let iu = ob
        .create_new_iu("ping", payload.clone(), false)
        .await
        .unwrap();
    iu.on_update(|iu| {
        let iu_copy = Arc::clone(&iu);
        Box::pin(async move {
            let iu = Arc::clone(&iu_copy);
            let mut payload = iu.get_payload().await;
            let count = payload.get("C").unwrap().as_u64().unwrap();
            println!("PING, {count}");
            payload["C"] = json!(count + 1);
            iu.set_payload(payload).await.unwrap();
        })
    })
    .await;
    println!("3");
    tokio::time::sleep(Duration::from_secs(3)).await;
    println!("4");
    ob.publish_iu(Arc::clone(&iu)).await.unwrap();
    //iu.set_payload(payload).await.unwrap();
    //iu.announce_change_over_backend().await.unwrap();
    println!("Lets go!");

    loop {
        tokio::time::sleep(Duration::from_secs(5)).await;
    }
}
