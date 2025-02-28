import asyncio

from ipaacar.components import create_mqtt_pair

from ipaacar.handler import MessageCallbackHandlerInterface


class MessageHandler(MessageCallbackHandlerInterface):
    """We inherit from a different ABC"""

    async def process_message_callback(self, msg: str):
        """We receive a str rather than an IU now"""
        print(msg)


async def msg_example():
    ib, ob = await create_mqtt_pair("ib_msg", "ob_msg", "me", "localhost:1883")
    await asyncio.gather(ib.listen_to_category("message_cat"),
                         ib.on_new_message(MessageHandler()))
    await ob.send_message("message_cat",
                          "Ich bin einmal durch den MQTT Broker gewandert!")
    await asyncio.sleep(1)  # necessary for the Rust coroutines to finish


loop = asyncio.get_event_loop()
loop.run_until_complete(msg_example())
