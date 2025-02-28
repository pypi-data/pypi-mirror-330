import abc

from ipaacar.components import IU


class IUCallbackHandlerInterface(abc.ABC):
    """
    Interface for IU callback handling. Used by the IU for update callback handling and the Input Buffer for new IUs.
    """

    @abc.abstractmethod
    async def process_iu_callback(self, iu: IU):
        """
        Will be awaited by Callbacks from inside the Rust event loop and send to the same
        Python event loop that was used for registering it.
        Any Exception will be logged on error level.

        :param iu: New/Updated IU
        :return: Nothing
        """
        pass


class MessageCallbackHandlerInterface(abc.ABC):

    @abc.abstractmethod
    async def process_message_callback(self, msg: str):
        pass
