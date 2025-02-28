import asyncio
import json
import time

from ipaacar.components import create_mqtt_pair, IU

from ipaacar.handler import IUCallbackHandlerInterface


class IUHandler(IUCallbackHandlerInterface):
    def __init__(self):
        self.start_time = time.time()

    async def process_iu_callback(self, iu: IU):
        c = json.loads(await iu.get_payload())
        if c["c"] == 10_000:
            print(time.time() - self.start_time)
            await asyncio.sleep(1)
            loop.stop()
        else:
            c["c"] += 1
            await iu.set_payload(json.dumps(c))


async def iu_example():
    c = json.dumps({"c": 0})
    ib, ob = await create_mqtt_pair("ib_msg", "ob_msg", "me", "localhost:1883")
    iu = await ob.create_new_iu("inc_message", c)
    await iu.add_callback(IUHandler())
    await iu.announce_change_over_backend()

loop = asyncio.get_event_loop()
loop.run_until_complete(iu_example())
loop.run_forever()
