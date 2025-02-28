import json
from tango.server import (
    AttrDataFormat,
    Device,
    attribute,
    command,
    device_property,
)
from tango import AttrQuality, AttrWriteType, DevState, DispLevel
from tango import GreenMode
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion, MQTTProtocolVersion
from datetime import datetime
from time import time
from dataclasses import dataclass
import builtins
import types


@dataclass
class MqttMessage:
    """MQTT message"""

    payload: str
    topic: str


class McMaxTangoDs(Device):
    """Tango device server to control MC-MAX microcontrollers thru MQTT"""

    green_mode = GreenMode.Asyncio

    # To connect to the MQTT server
    broker = device_property(dtype=str, default_value="localhost")
    username = device_property(dtype=str, default_value="")
    password = device_property(dtype=str, default_value="")
    mqtt_name = device_property(dtype=str, default_value="")

    firmware_name = attribute(dtype=str, display_level=DispLevel.EXPERT)
    firmware_version = attribute(dtype=str, display_level=DispLevel.EXPERT)

    async def init_device(self):
        self.mc_attributes_description = []
        self.rec_messages: list[MqttMessage] = []
        self.old_attributes = []
        self.old_commands = []
        self.max_msg_circular_buffer = 10
        self.last_received_values = {}
        self.conversions = {}
        self._firmware_name = ""
        self._firmware_version = ""

        await super().init_device()
        self.info_stream("Connecting to MQTT server")
        self.set_state(DevState.INIT)
        self.set_status(
            f"Initialization started {datetime.now()}.\nTrying to connect."
        )

        # Creating a client instance
        self.mqtt = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            protocol=MQTTProtocolVersion.MQTTv5,
        )
        try:
            self.connect()
        except Exception as exc:
            msg = f"Error connecting to the MQTT server: {exc}"
            self.error_stream(msg)
            self.set_state(DevState.FAULT)
            self.set_status(msg)
            return

        # Subscribe to firmware name
        topic = f"mc_max/{self.mqtt_name}/firmware_name"
        self.mqtt.subscribe(topic=topic)
        self.mqtt.message_callback_add(
            sub=topic, callback=self.process_firmware_name
        )

        # Subscribe to firmware version
        topic = f"mc_max/{self.mqtt_name}/firmware_version"
        self.mqtt.subscribe(topic=topic)
        self.mqtt.message_callback_add(
            sub=topic, callback=self.process_firmware_version
        )

        topic = f"mc_max/{self.mqtt_name}/tango_attributes"
        self.mqtt.subscribe(topic=topic)
        self.mqtt.message_callback_add(
            sub=topic, callback=self.process_attributes_self_description
        )

        topic = f"mc_max/{self.mqtt_name}/tango_commands"
        self.mqtt.subscribe(topic=topic)
        self.mqtt.message_callback_add(
            sub=topic, callback=self.process_commands_self_description
        )

        # TODO mc should be able to publish tango state
        self.set_status(
            f"Initialization completed {datetime.now()}.\n"
            "Waiting for Microcontroller self description..."
        )

    # MQTT connection
    def connect(self):
        self.mqtt.username_pw_set(
            username=self.username, password=self.password
        )
        self.mqtt.connect(host=self.broker)
        self.mqtt.loop_start()

    def process_firmware_name(self, client, userdata, msg):
        self._firmware_name = msg.payload

    def process_firmware_version(self, client, userdata, msg):
        self._firmware_version = msg.payload

    def process_attributes_self_description(self, client, userdata, msg):
        # load as JSON
        try:
            self.mc_attributes_description = json.loads(msg.payload)
        except Exception as exc:
            msg = (
                "Error in microcontroller self description: "
                f"Exception was: {exc}"
            )
            self.error_stream(msg)
            raise RuntimeError(msg)

        # Clean up old attributes
        for old_attribute in self.old_attributes:
            try:
                self.remove_attribute(old_attribute)
            except Exception:
                self.warn_stream(
                    f"Tried to remove attribute {attribute} "
                    "without success, ignoring."
                )
        self.old_attributes = []

        # Process the list of attribute dictionaries
        for new_attribute in self.mc_attributes_description:
            if "access" in new_attribute:
                new_attribute["access"] = getattr(
                    AttrWriteType, new_attribute["access"]
                )
            if "display_level" in new_attribute:
                new_attribute["display_level"] = getattr(
                    DispLevel, new_attribute["display_level"]
                )
            if "dformat" in new_attribute:
                new_attribute["dformat"] = getattr(
                    AttrDataFormat, new_attribute["dformat"]
                )
            attr = attribute(**new_attribute)
            if attr.attr_write in [
                AttrWriteType.READ_WRITE,
                AttrWriteType.WRITE,
                AttrWriteType.READ_WITH_WRITE,
            ]:
                write_method = self.generic_write
            else:
                write_method = None
            self.add_attribute(
                attr, r_meth=self.generic_read, w_meth=write_method
            )

            self.old_attributes.append(attr.name)
            try:
                _dtype = new_attribute["dtype"]
                if _dtype == "bool":
                    self.conversions[attr.name] = self.str2bool
                else:
                    self.conversions[attr.name] = getattr(builtins, _dtype)
            except KeyError:
                msg = (
                    "Error in microcontroller self description: no dtype "
                    f"specified for attribute {attr.name}"
                )
                self.error_stream(msg)
                raise RuntimeError(msg)

            self.set_change_event(attr.name, True)
            mc_output_data_topic = (
                f"mc_max/{self.mqtt_name}/mc_output/{attr.name}"
            )
            self.mqtt.subscribe(topic=mc_output_data_topic)
            self.debug_stream(f"Subscribing to {mc_output_data_topic}")

            def generic_event_pusher(client, userdata, msg):
                # get attribute name
                att_name = msg.topic.split("/")[-1]
                try:
                    conversion_function = self.conversions[att_name]
                    value = conversion_function(msg.payload.decode("utf-8"))
                    quality = AttrQuality.ATTR_VALID
                    self.last_received_values[att_name] = value
                    self.debug_stream(f"{att_name} = {value}")
                except AttributeError:
                    # The dtype is not a builtin
                    self.last_received_values[att_name] = None
                    msg = (
                        "Error in microcontroller self description: dtype "
                        f"{self.conversions[att_name]} for attribute "
                        f"{att_name} does not match any python "
                        "builtin data type"
                    )
                    self.error_stream(msg)
                    # In this case, we interrupt the code flow
                    # because we don't even know what dtype we should push
                    raise RuntimeError(msg)
                except Exception as exc:
                    self.last_received_values[att_name] = None
                    # trick to have a placeholder value of correct type
                    # Must be set to ATTR_INVALID
                    value = conversion_function()
                    quality = AttrQuality.ATTR_INVALID
                    self.error_stream(
                        f"Could not translate value {value} for attribute "
                        f"{att_name}, exception was {exc}"
                    )
                self.push_change_event(att_name, value, time(), quality)

            # give this function a unique name and make it an attribute
            specific_callback_name = f"{attr.name}_event_pusher"
            setattr(self, specific_callback_name, generic_event_pusher)
            self.mqtt.message_callback_add(
                sub=mc_output_data_topic,
                callback=getattr(self, specific_callback_name),
            )
        if self.dev_state() is DevState.INIT:
            # here if first self description received since init
            self.set_state(DevState.ON)
            self.set_status(
                f"Microcontroller description received {datetime.now()}.\n"
                "Device operating normally."
            )

    def _create_method(self, name):
        @command(dtype_in=str)
        async def dynamic_method(self, parameters):
            topic = f"mc_max/{self.mqtt_name}/command/{name}"
            payload = parameters
            self.mqtt.publish(topic=topic, payload=payload)

        dynamic_method.__name__ = name

        return dynamic_method

    def process_commands_self_description(self, client, userdata, msg):
        # load as JSON
        try:
            self.mc_commands_description = json.loads(msg.payload)
        except Exception as exc:
            msg = (
                "Error in microcontroller commands self description: "
                f"Exception was: {exc}"
            )
            self.error_stream(msg)
            raise RuntimeError(msg)

        # Clean up old commands
        for old_command in self.old_commands:
            try:
                self.remove_command(old_command)
            except Exception:
                self.warn_stream(
                    f"Failed to remove command {old_command}. " "Ignoring it"
                )
        self.old_commands = []

        # Process the list of attribute dictionaries
        for new_command in self.mc_commands_description:
            setattr(
                self,
                new_command["name"],
                types.MethodType(
                    self._create_method(new_command["name"]), self
                ),
            )
            self.add_command(getattr(self, new_command["name"]))
            self.old_commands.append(new_command["name"])

    async def generic_read(self, attr):
        self.debug_stream(f"Generic read for attribute {attr.get_name()}")
        if attr.get_name() not in self.last_received_values:
            attr.set_quality(AttrQuality.ATTR_INVALID)
            return
        return self.last_received_values[attr.get_name()]

    async def generic_write(self, attr):
        topic = f"mc_max/{self.mqtt_name}/mc_input/{attr.get_name()}"
        payload = str(attr.get_write_value())
        self.mqtt.publish(topic=topic, payload=payload)

    async def read_firmware_version(self):
        return self._firmware_version

    async def read_firmware_name(self):
        return self._firmware_name

    def str2bool(self, data: str) -> bool:
        if data.lower() in ("true", "yes", "on", "1"):
            return True
        else:
            return False


def main():
    McMaxTangoDs.run_server()


if __name__ == "__main__":
    main()
