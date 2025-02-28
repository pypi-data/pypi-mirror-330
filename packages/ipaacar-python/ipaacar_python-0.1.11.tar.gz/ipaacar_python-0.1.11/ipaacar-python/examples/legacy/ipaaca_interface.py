import syslog
import asyncio

from ipaacar.components import InputBuffer, OutputBuffer, IU

from ipaacar.handler import IUCallbackHandlerInterface





class IpaacaInterface:

    def __init__(self, name, outgoing_categories=None, incoming_categories=None):
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.output_buffer = self.loop.run_until_complete(
            OutputBuffer.new_with_connect(name + '_OutputBuffer', name, "localhost:1883")
        )

        self.outgoing_categories = []
        self.incoming_categories = []

        if outgoing_categories is not None:
            for category in outgoing_categories:
                self.outgoing_categories.append(category)

        if incoming_categories is not None:
            for category in incoming_categories:
                self.incoming_categories.append(category)

        if incoming_categories:
            self.input_buffer = self.loop.run_until_complete(
                InputBuffer.new_with_connect(name + '_InputBuffer', name, "localhost:1883")
            )
            for category in self.incoming_categories:
                self.loop.run_until_complete(self.input_buffer.listen_to_category(category))
            # self.input_buffer.set_resend_active() ????
            # self.input_buffer.register_handler(
            #    self.incoming_iu_handler)  # no idea what these 2 lines do

        syslog.syslog(syslog.LOG_NOTICE, "Outgoing IPAACA categories " + ', '.join(self.outgoing_categories))
        syslog.syslog(syslog.LOG_NOTICE, "Incoming IPAACA categories " + ', '.join(self.incoming_categories))

    def is_to_be_ignored(self, event_type):
        ignore_flag = False
        # if event_type in [ipaaca.iu.IUEventType.COMMITTED, ipaaca.iu.IUEventType.DELETED,
        #                   ipaaca.iu.IUEventType.RETRACTED]:
        #    ignore_flag = True
        return ignore_flag

    # Override in subclasses
    def incoming_iu_handler(self, iu, event_type, local):
        syslog.syslog(syslog.LOG_NOTICE, "Received message for category: " + iu.category)

    def retract_iu(self, iu=None):
        if iu is not None:
            self.output_buffer.remove(iu)
            syslog.syslog(syslog.LOG_NOTICE,
                          "IU with UID " + iu.uid + " has been removed from OutputBuffer " + self.output_buffer.unique_name + '.')

    # Use this if a new IPAACA IU is to be sent every time
    def create_and_send_outgoing_iu(self, category, data, add_link=False, link_type="", iu_id_to_link=None):
        if data is not None and type(data).__name__ != 'dict' and type(data).__name__ != 'OrderedDict' and type(
                data).__name__ != 'list':
            syslog.syslog(syslog.LOG_ERR,
                          self.name + "reports \'Data provided is not in dictionary or list format.\' Therefore, "
                                      "no IU sent. The data was provided in format: " + type(
                              data).__name__)
            return None

        if category not in self.outgoing_categories:
            syslog.syslog(syslog.LOG_NOTICE,
                          self.name + " reports \'Unregistered outgoing IPAACA category:\' " + category + ". It will now be added to registered IPAACA categories.")
            self.outgoing_categories.append(category)

        iu = ipaaca.IU(category)
        iu.payload = data or {}
        if add_link is True:
            if iu_id_to_link != None:
                iu.add_links(link_type, iu_id_to_link, self.name)
            else:
                syslog.syslog(syslog.LOG_ERR,
                              self.name + "reports \'The IU to be linked is not specified. Therefore, no links added.\'")
        self.output_buffer.add(iu)
        syslog.syslog(syslog.LOG_NOTICE, 'IU ' + str(iu.uid) + ' for category ' + category + ' sent.')

        return iu

    # Use this if an existing IU is to be updated
    def update_and_send_outgoing_iu(self, category, data, iu=None):
        if iu is None:
            syslog.syslog(syslog.LOG_NOTICE,
                          self.name + " reports \'No IU object specified.\' Therefore, redirecting to create_and_send_iu.")
            iu = self.create_and_send_outgoing_iu(category, data)
            return iu

        if iu is not None and type(iu).__name__ != 'IU':
            syslog.syslog(syslog.LOG_ERR,
                          self.name + " reports \'The provided argument is not of type IU.\ Therefore, no IU update sent.")
            return iu

        if iu.category != category:
            syslog.syslog(syslog.LOG_ERR,
                          self.name + " reports \'The provided category and the category of the IU do not match.\ Therefore, no IU update sent.")
            return iu

        if data is not None and type(data).__name__ != 'dict' and type(data).__name__ != 'OrderedDict' and type(
                data).__name__ != 'list':
            syslog.syslog(syslog.LOG_ERR,
                          self.name + " reports \'Data provided is not in dictionary or list format.\' Therefore, no IU sent. The data was provided in format: " + type(
                              data).__name__)
            return iu

        if iu.category not in self.outgoing_categories:
            syslog.syslog(syslog.LOG_NOTICE,
                          self.name + " reports \'Unregistered outgoing IPAACA category:\' " + category + ". It will now be added to registered IPAACA categories.")
            self.outgoing_categories.append(category)

        iu.payload = data  # TODO: Will this work if the payload contains many items? How to combine with 'with' statement? Here insert a check if data has changed from what is stored in the IU

        if not iu.is_published:
            self.output_buffer.add(iu)
        # The iu argument received is updated and is available in the calling function.

        syslog.syslog(syslog.LOG_NOTICE, 'IU Update sent for category ' + category + '.')
        return iu

    # Use this if a new IPAACA message is to be sent every time
    def create_and_send_outgoing_msg(self, category, data):
        if data is not None and type(data).__name__ != 'dict' and type(data).__name__ != 'OrderedDict' and type(
                data).__name__ != 'list':
            syslog.syslog(syslog.LOG_ERR,
                          self.name + " reports \'Data provided is not in dictionary or list format.\' Therefore, no Message sent. The data was provided in format: " + type(
                              data).__name__)
            return None

        if category not in self.outgoing_categories:
            syslog.syslog(syslog.LOG_NOTICE,
                          self.name + " reports \'Unregistered outgoing IPAACA category:\' " + category + ". It will now be added to registered IPAACA categories.")
            self.outgoing_categories.append(category)

        msg = ipaaca.Message(category)
        msg.payload = data or {}

        self.output_buffer.add(msg)
        syslog.syslog(syslog.LOG_NOTICE, 'Message ' + str(msg.uid) + ' for category ' + category + ' sent.')


class CompatibilityIUHandler(IUCallbackHandlerInterface):

    def __init__(self, ipaaca_interface: IpaacaInterface):
        self.ipaaca = ipaaca_interface
    async def process_iu_callback(self, iu: IU):
        pass