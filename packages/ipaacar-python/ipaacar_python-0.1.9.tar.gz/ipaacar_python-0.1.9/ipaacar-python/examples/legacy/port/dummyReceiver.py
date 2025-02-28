from ipaacar.legacy import IpaacaInterface


class Handler(IpaacaInterface):

    def __init__(self, name, incoming_categories):
        super().__init__(name, outgoing_categories=[], incoming_categories=incoming_categories)

    async def async_incoming_msg_handler(self, message: str):
        print(message)


handler = Handler("_PerceptionInterface", ["UserInfo"])
handler.loop.run_forever()
