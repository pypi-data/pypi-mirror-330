import asyncio
import json
import time

from ipaacar.components import create_mqtt_pair, IU

from ipaacar.handler import IUCallbackHandlerInterface


class IUHandler(IUCallbackHandlerInterface):
    def __init__(self, i, vals):
        self.i = i
        self.vals = vals

    async def process_iu_callback(self, iu: IU):
        c = json.loads(await iu.get_payload())
        if c["c"] == 500:
            self.vals[self.i] = True
        else:
            c["c"] += 1
            await iu.set_payload(json.dumps(c))


num_ius = 20


async def end_checker(vals: list[bool]):
    start_time = time.time()
    while not all(vals):
        # we need to sleep here/await something,
        # so that the eventloop can switch coroutines
        await asyncio.sleep(.1)
    print(time.time() - start_time)
    await asyncio.sleep(1)
    loop.stop()


async def iu_example():
    c = json.dumps({"c": 0})
    ib, ob = await create_mqtt_pair("ib_msg", "ob_msg", "me", "localhost:1883")
    vals = [False] * num_ius
    ius: list[IU] = await asyncio.gather(*[ob.create_new_iu(f"inc_message_{i}", c)
                                           for i in range(num_ius)])
    await asyncio.gather(*[ius[i].add_callback(IUHandler(i, vals))
                           for i in range(num_ius)])
    loop.create_task(end_checker(vals))
    await asyncio.gather(*[ius[i].announce_change_over_backend()
                           for i in range(num_ius)])


loop = asyncio.get_event_loop()
loop.run_until_complete(iu_example())
loop.run_forever()
