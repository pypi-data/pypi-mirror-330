import random
import time
import uuid

from scs_architecture.definitions import UserInfo

from ipaacar.legacy import IpaacaInterface

NAMES = (
    "Sonja", "Stefan", "Amelie", "Niklas", "Hendric", "Sebastian", "Olga", "Benedikt", "Victoria", "Lina", "Dagmar",
    "Jan")


class _PerceptionInterface(IpaacaInterface):

    def __init__(self, name, component):
        # Usually the string is used for the categories, but using the class would be better imo
        super(_PerceptionInterface, self).__init__(name, outgoing_categories=[UserInfo.__name__],
                                                   incoming_categories=[])
        self.perception_component = component


class DummyPerception:

    def __init__(self):
        self.interface = _PerceptionInterface("_PerceptionInterface", self)

    def run(self):
        while True:
            user_info = UserInfo(uuid=str(uuid.uuid1()),
                                 info={"name": random.choice(NAMES), "birthday": "", "hoobies": "", "interests": "",
                                       "skills": ""})
            print("new person: ", user_info)
            self.interface.create_and_send_outgoing_msg(category=UserInfo.__name__, data=user_info._asdict())
            time.sleep(1)


if __name__ == "__main__":
    instance = DummyPerception()
    instance.run()
