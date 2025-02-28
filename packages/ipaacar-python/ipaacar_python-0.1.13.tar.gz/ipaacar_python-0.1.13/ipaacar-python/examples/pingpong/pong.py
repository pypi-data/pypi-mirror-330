import asyncio
import json

from ipaacar.components import IU, create_mqtt_pair

from ipaacar.handler import IUCallbackHandlerInterface


class PongHandler(IUCallbackHandlerInterface):

    def __init__(self):
        self.ping_iu: IU | None = None

    async def process_iu_callback(self, iu: IU):
        if self.ping_iu is not None:
            payload = await iu.get_payload()
            p_dict = json.loads(payload)
            p_dict["counter"] += 1
            payload = json.dumps(p_dict)
            print(payload)
            await self.ping_iu.set_payload(payload)
        else:
            print("no ping yet")


class NewPingReceived(IUCallbackHandlerInterface):

    def __init__(self, ph: PongHandler):
        self.ph = ph

    async def process_iu_callback(self, iu: IU):
        self.ph.ping_iu = iu


async def pong():
    ib, ob = await create_mqtt_pair("pong_ib", "pong_ob", "PingPong", "localhost:1883")
    pong_handler = PongHandler()
    await asyncio.gather(ib.listen_to_category("ping"),
                         ib.on_new_iu(NewPingReceived(pong_handler)))
    init_payload = {"counter": "initialized by ping"}
    iu = await ob.create_new_iu("pong", json.dumps(init_payload))
    await iu.add_callback(pong_handler)
    # await iu.announce_change_over_backend()


loop = asyncio.get_event_loop()
loop.run_until_complete(pong())
loop.run_forever()
