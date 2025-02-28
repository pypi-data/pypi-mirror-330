import asyncio
import json
import time

from ipaacar.components import IU, OutputBuffer

from ipaacar.handler import IUCallbackHandlerInterface


class IUHandler(IUCallbackHandlerInterface):
    def __init__(self, iu_idx, buffer_idx, vals):
        self.iu_idx = iu_idx
        self.buffer_idx = buffer_idx
        self.vals = vals

    def get_iu_array_index(self):
        return self.buffer_idx * num_ius + self.iu_idx

    async def process_iu_callback(self, iu: IU):
        c = json.loads(await iu.get_payload())
        if c["c"] == 100:
            self.vals[self.get_iu_array_index()] = True
        else:
            c["c"] += 1
            await iu.set_payload(json.dumps(c))


num_ius = 20
num_buffer = 5


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
    buffers = await asyncio.gather(
        *[OutputBuffer.new_with_connect(f"buffer_{i}", "mult_buffer", "localhost:1883")
          for i in range(num_buffer)])
    vals = [False] * (num_ius * num_buffer)
    await asyncio.sleep(1)
    ius_futures = []
    for ob_idx, ob in enumerate(buffers):
        for iu_idx in range(num_ius):
            ius_futures.append(ob.create_new_iu(f"inc_message_{iu_idx}_{ob_idx}", c))
    ius: list[IU] = await asyncio.gather(*ius_futures)

    for ob_idx, ob in enumerate(buffers):
        for iu_idx in range(num_ius):
            await ius[ob_idx * num_ius + iu_idx].add_callback(
                IUHandler(iu_idx, ob_idx, vals))
    await asyncio.sleep(1)
    loop.create_task(end_checker(vals))
    await asyncio.gather(*[iu.announce_change_over_backend() for iu in ius])


loop = asyncio.get_event_loop()
loop.run_until_complete(iu_example())
loop.run_forever()
