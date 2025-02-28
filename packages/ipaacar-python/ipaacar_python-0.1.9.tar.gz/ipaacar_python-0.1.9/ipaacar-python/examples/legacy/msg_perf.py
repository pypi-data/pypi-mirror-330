import time

from ipaacatools.scripts.ipaaca_interface import IpaacaInterface


class IUTest(IpaacaInterface):

    def __init__(self, name, outgoing_categories, incoming_categories):
        super().__init__(name, outgoing_categories, incoming_categories)
        self.time = time.time()

    def incoming_iu_handler(self, iu, event_type, local):
        data = iu.payload
        if data["c"] == 10_000:
            print(time.time() - self.time)
            exit(69)
        else:
            data["c"] += 1
            self.create_and_send_outgoing_msg("c_msg", {"c": data["c"]})


iu_test = IUTest("IUTest", ["c_msg"], ["c_msg"])
iu_test.create_and_send_outgoing_msg("c_msg", {"c": 0})

while True:
    pass
