from ipaacar.handler import IUCallbackHandlerInterface, MessageCallbackHandlerInterface


class IU:

    def __new__(cls, category: str, component_name: str, payload: str) -> IU:
        ...

    async def get_category(self) -> str:
        ...

    async def get_uid(self) -> str:
        ...

    async def get_owner_buffer_uid(self) -> str | None:
        ...

    async def is_committed(self) -> bool:
        ...

    async def get_payload(self) -> str:
        ...

    async def get_component_name(self) -> str:
        ...

    async def get_links(self) -> dict[str, list[str]]:
        ...

    async def set_payload(self, payload: str):
        ...

    async def add_target_to_link(self, link_name: str, target: str):
        ...

    async def remove_target_from_link(self, link_name: str, target: str):
        ...

    async def remove_link(self, link_name: str):
        ...

    async def add_callback(self, callback: IUCallbackHandlerInterface):
        ...

    async def announce_change_over_backend(self):
        ...


class OutputBuffer:

    @classmethod
    async def new_with_connect(cls, uid: str, component_name: str, address: str) -> OutputBuffer:
        ...

    async def create_new_iu(self, category: str, payload: str) -> IU:
        ...

    async def publish_iu(self, iu: IU):
        ...

    async def commit_iu(self, iu: IU):
        ...

    async def send_message(self, topic: str, message: str):
        ...


class InputBuffer:

    @classmethod
    async def new_with_connect(cls, uid: str, component_name: str, address: str) -> InputBuffer:
        ...

    async def get_received_iu_ids(self) -> list[str]:
        ...

    async def get_iu_by_id(self, uid: str) -> IU:
        ...

    async def get_all_ius(self) -> list[IU]:
        ...

    async def listen_to_category(self, category: str):
        ...

    async def on_new_iu(self, callback_handler: IUCallbackHandlerInterface):
        ...

    async def on_new_message(self, callback_handler: MessageCallbackHandlerInterface):
        ...

async def create_mqtt_pair(input_uid: str, output_uid: str, component_name: str, address: str) -> tuple[
    InputBuffer, OutputBuffer]:
    ...
