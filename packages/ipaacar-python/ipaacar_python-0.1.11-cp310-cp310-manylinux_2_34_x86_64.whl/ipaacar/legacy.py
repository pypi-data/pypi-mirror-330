"""
This submodule contains code that should not be used in new projects and only
serves as a compatibility layer for code that was written for the old pure-python version.
"""
import asyncio
import json
import logging

import nest_asyncio
from ipaacar.components import IU, OutputBuffer, InputBuffer

from ipaacar.handler import IUCallbackHandlerInterface, MessageCallbackHandlerInterface

nest_asyncio.apply()


class IpaacaInterface:
    """
    Defines an IPAACA component. That is, a component that uses IPAACA to send and receive messages.

    Args:
       name (:obj:'str'): name of the component
       outgoing_categories ([] of :obj:'str'): names of outgoing IPAACA categories
       incoming_categories ([] of :obj:'str'): names of incoming IPAACA categories
    """

    def __init__(self, name, outgoing_categories=None, incoming_categories=None):
        self.loop = asyncio.new_event_loop()
        self.name = name
        self.loop.run_until_complete(self.async_init(name, outgoing_categories, incoming_categories))

    async def async_init(self, name, outgoing_categories=None, incoming_categories=None):
        self.output_buffer = await OutputBuffer.new_with_connect(name + '_OutputBuffer', name, "localhost:1883")

        self.outgoing_categories = []
        self.incoming_categories = []

        if outgoing_categories is not None:
            for category in outgoing_categories:
                self.outgoing_categories.append(category)

        if incoming_categories is not None:
            for category in incoming_categories:
                self.incoming_categories.append(category)

        if incoming_categories:
            self.input_buffer = await InputBuffer.new_with_connect(name + '_InputBuffer', name, "localhost:1883")
            await asyncio.gather(*[self.input_buffer.listen_to_category(cat) for cat in incoming_categories])
            await self.input_buffer.on_new_iu(IUInputCompatibilityHandler(self))
            await self.input_buffer.on_new_message(MessageInputCompatibilityHandler(self))

        logging.info("Outgoing IPAACA categories " + ', '.join(self.outgoing_categories))
        logging.info("Incoming IPAACA categories " + ', '.join(self.incoming_categories))

    def is_to_be_ignored(self, event_type):
        return NotImplementedError("Not supported in new interface.")

    # Override in subclasses
    def incoming_iu_handler(self, iu, event_type, local):
        self.loop.run_until_complete(self.async_incoming_iu_handler(iu))

    async def async_incoming_iu_handler(self, iu):
        logging.info("Received IU for category: " + self.loop.run_until_complete(iu.get_category()))

    def incoming_msg_handler(self, message: str):
        self.loop.run_until_complete(self.async_incoming_msg_handler(message))

    async def async_incoming_msg_handler(self, message: str):
        logging.info("Received Message :" + message)

    def retract_iu(self, iu=None):
        return NotImplementedError("Not supported in new interface.")

    # Use this if a new IPAACA IU is to be sent every time
    def create_and_send_outgoing_iu(self, category, data, add_link=False, link_type="", iu_id_to_link=None):
        self.loop.run_until_complete(
            self.async_create_and_send_outgoing_iu(category, data, add_link, link_type, iu_id_to_link))

    async def async_create_and_send_outgoing_iu(self, category, data, add_link=False, link_type="", iu_id_to_link=None):
        string_data = json.dumps(data)
        iu = IU(category, self.name, string_data)
        if add_link is True:
            if iu_id_to_link is not None:
                await iu.add_target_to_link(link_type, iu_id_to_link)

        await self.output_buffer.publish_iu(iu)

        iu_id = await iu.get_uid()
        logging.info('IU ' + str(iu_id) + ' for category ' + category + ' sent.')

        return iu

    # Use this if an existing IU is to be updated
    def update_and_send_outgoing_iu(self, category, data, iu=None):
        self.loop.run_until_complete(self.async_update_and_send_outgoing_iu(category, data, iu))

    async def async_update_and_send_outgoing_iu(self, category, data, iu=None):
        string_data = json.dumps(data)
        await iu.set_payload(string_data)
        # we can't change the category of an IU. makes no sense.
        actual_category = await iu.get_category()
        logging.info('IU Update sent for category ' + actual_category + '.')
        return iu

    # Use this if a new IPAACA message is to be sent every time
    def create_and_send_outgoing_msg(self, category, data):
        self.loop.run_until_complete(self.async_create_and_send_outgoing_msg(category, data))

    async def async_create_and_send_outgoing_msg(self, category, data):
        if category not in self.outgoing_categories:
            logging.info(
                self.name + " reports \'Unregistered outgoing IPAACA category:\' " +
                category + ". It will now be added to registered IPAACA categories.")
            self.outgoing_categories.append(category)

        data = json.dumps(data)
        await self.output_buffer.send_message(category, data)
        logging.info('Message ' + data + ' for category ' + category + ' sent.')


class IUInputCompatibilityHandler(IUCallbackHandlerInterface):

    def __init__(self, interface_deriver: IpaacaInterface):
        self.ipaaca = interface_deriver

    async def process_iu_callback(self, iu: IU):
        self.ipaaca.incoming_iu_handler(iu, None, False)


class MessageInputCompatibilityHandler(MessageCallbackHandlerInterface):

    def __init__(self, interface_deriver: IpaacaInterface):
        self.ipaaca = interface_deriver

    async def process_message_callback(self, msg: str):
        self.ipaaca.incoming_msg_handler(msg)
