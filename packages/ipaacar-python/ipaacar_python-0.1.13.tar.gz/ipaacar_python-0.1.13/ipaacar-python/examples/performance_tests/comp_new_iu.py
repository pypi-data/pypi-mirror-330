import asyncio
import json
import time

from ipaacar.components import create_mqtt_pair, IU, OutputBuffer

from ipaacar.handler import IUCallbackHandlerInterface


class IUHandler(IUCallbackHandlerInterface):
    def __init__(self, ob: OutputBuffer):
        self.start_time = time.time()
        self.ob = ob

    async def process_iu_callback(self, iu: IU):
        c = json.loads(await iu.get_payload())
        if c["c"] == 10_000:
            print(time.time() - self.start_time)
            await asyncio.sleep(1)
            loop.stop()
        else:
            c["c"] += 1
            await self.ob.create_new_iu("inc_message", json.dumps(c))


async def iu_example():
    c = json.dumps({"c": 0})
    ib, ob = await create_mqtt_pair("ib_msg", "ob_msg", "me", "localhost:1883")
    _, iu, _ = await asyncio.gather(ib.listen_to_category("inc_message"),
                                    ob.create_new_iu("inc_message", c),
                                    ib.on_new_iu(IUHandler(ob)))
    await iu.announce_change_over_backend()


loop = asyncio.get_event_loop()
loop.run_until_complete(iu_example())
loop.run_forever()
