import asyncio
import json

from ipaacar.components import IU, create_mqtt_pair

from ipaacar.handler import IUCallbackHandlerInterface


class PingHandler(IUCallbackHandlerInterface):
    """
    First we define a PingHandler.
    This class inherits from the IUCallbackHandlerInterface
    and defines the Logic, that should happen an IU receives
    an update.
    """

    def __init__(self):
        """
        Since we want to update the Pong IU once we receive an update on our ping IU,
        we create a field for it.
        pong_iu is none, as long as the input buffer didn't receive it.
        """
        self.pong_iu: IU | None = None

    async def process_iu_callback(self, iu: IU):
        """
        The callback will call THIS method, when the Ping IU is updated.

        Here we parse the payload,
        increment the counter
        and update the Pong IU with the new counter.

        :param iu: Our updated Ping IU.
        """
        if self.pong_iu is not None:
            payload = await iu.get_payload()
            p_dict = json.loads(payload)
            p_dict["counter"] += 1
            payload = json.dumps(p_dict)
            print(payload)
            await self.pong_iu.set_payload(payload)
        else:
            print("no pong yet")


class NewPongReceived(IUCallbackHandlerInterface):
    """
    This IU Callback Handler is for the InputBuffer.
    It determines what we want to ddo with newly received IUs.
    """

    def __init__(self, ph: PingHandler):
        """
        We want to update the Pong IU in our PingHandler.
        That's wy we create a field for it.
        :param ph: The PingHandler that is responsible for the Ping IU updates.
        """
        self.ph = ph

    async def process_iu_callback(self, iu: IU):
        """
        Here we just set the pong_iu in the Ping Update Callback.
        :param iu: The newly received pong IU.
        """
        self.ph.pong_iu = iu


async def ping():
    # create buffers
    ib, ob = await create_mqtt_pair("ping_ib", "ping_ob", "PingPong", "localhost:1883")
    # Create Ping Callback Handler
    ping_handler = PingHandler()
    # concurrently add category listener and Callback
    await asyncio.gather(ib.listen_to_category("pong"),
                         ib.on_new_iu(NewPongReceived(ping_handler)))
    init_payload = {"counter": 0}
    # directly create IU that is placed into an OutputBuffer
    iu = await ob.create_new_iu("ping", json.dumps(init_payload))
    # register the Callback for the IU update
    await iu.add_callback(ping_handler)
    # wait for pong to get rdy
    await asyncio.sleep(1)
    # trigger a dummy update to start update circle
    await iu.announce_change_over_backend()


# asyncio stuff to run ping()
loop = asyncio.get_event_loop()
loop.run_until_complete(ping())
# this is necessary, because asyncio can't keep track
# of the rust Callbacks running in the Background,
# that trigger updates
loop.run_forever()
