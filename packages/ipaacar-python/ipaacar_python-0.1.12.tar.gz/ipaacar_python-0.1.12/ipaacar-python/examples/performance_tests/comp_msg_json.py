import asyncio
import json
import time

from ipaacar.components import create_mqtt_pair, OutputBuffer

from ipaacar.handler import MessageCallbackHandlerInterface


class MessageHandler(MessageCallbackHandlerInterface):
    def __init__(self, ob: OutputBuffer):
        self.ob = ob
        self.start_time = time.time()

    async def process_message_callback(self, msg: str):
        c = json.loads(msg)
        if c["c"] == 10_000:
            print(time.time() - self.start_time)
            loop.stop()
        else:
            c["c"] += 1
            await self.ob.send_message("inc_message", json.dumps(c))


async def msg_example():
    c = json.dumps({"c": 0})
    ib, ob = await create_mqtt_pair("ib_msg", "ob_msg", "me", "localhost:1883")
    await asyncio.gather(ib.listen_to_category("inc_message"),
                         ib.on_new_message(MessageHandler(ob)))
    await ob.send_message("inc_message", c)


loop = asyncio.get_event_loop()
loop.run_until_complete(msg_example())
loop.run_forever()
