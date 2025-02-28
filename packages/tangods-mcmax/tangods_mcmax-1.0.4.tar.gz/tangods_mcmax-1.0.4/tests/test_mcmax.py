import pytest
import json
from tango import DevState
from tango.server import command
from tango.test_context import DeviceTestContext
from unittest.mock import patch

# Import tango DS
from mcmax import McMaxTangoDs, MqttMessage


MQTT_NAME = "test"


@pytest.fixture
def deviceProxy():
    device = DeviceTestContext(
        McMaxTangoDs,
        properties={
            "broker": "localhost",
            "username": "user",
            "password": "password",
            "mqtt_name": MQTT_NAME,
        },
        process=True,
    )
    yield device


def testImport():
    """Test importation of the Tango DS"""
    from mcmax import McMaxTangoDs  # noqa: F401


@patch("mcmax.mcmax.Client")
def testInit(mocker, deviceProxy):
    """Test device goes into INIT when initialised"""
    with deviceProxy as proxy:
        assert proxy.status().startswith("Initialization completed")
        assert proxy.state() == DevState.INIT


@patch(
    "mcmax.mcmax.Client.username_pw_set",
    side_effect=ValueError("PROBLEM"),
)
def testConnectionFailed(mocker, deviceProxy):
    """Test device failed to connect to the MQTT broker"""
    with deviceProxy as proxy:
        assert proxy.state() == DevState.FAULT
        assert proxy.status() == "Error connecting to the MQTT server: PROBLEM"


def testProcessingFirmware():
    """Test device can process firmware information"""

    # Process the messages
    McMaxTangoDs.process_firmware_name(
        McMaxTangoDs,
        None,
        None,
        MqttMessage(
            topic=f"mc_max/{MQTT_NAME}/firmware_name", payload="TestFirmware"
        ),
    )
    McMaxTangoDs.process_firmware_version(
        McMaxTangoDs,
        None,
        None,
        MqttMessage(
            topic=f"mc_max/{MQTT_NAME}/firmware_version", payload="1.0.0"
        ),
    )

    # Assert values
    assert McMaxTangoDs._firmware_name == "TestFirmware"
    assert McMaxTangoDs._firmware_version == "1.0.0"


def testProcessingAttributesSelfDescription():
    """Test device can receive attribute self-description information"""

    class MqttMessageRaw:
        topic = ""
        payload = None

        def __init__(self, topic, payload):
            self.topic = topic
            self.payload = payload

    class TestDev(McMaxTangoDs):
        @command(dtype_in=str)
        async def test_process_attribute_self_description(self, string):
            msg = MqttMessage(payload=string, topic="test/notopic")
            self.process_attributes_self_description(None, None, msg)

        @command(dtype_in=float)
        async def test_add_fake_voltage_value(self, value):
            msg = MqttMessageRaw(
                topic=f"mc_max/{MQTT_NAME}/mc_output/voltage",
                payload=str(value).encode("ascii"),
            )
            self.voltage_event_pusher(None, None, msg)

    with DeviceTestContext(
        TestDev,
        properties={
            "broker": "localhost",
            "username": "user",
            "password": "password",
            "mqtt_name": MQTT_NAME,
        },
        process=True,
    ) as device:

        attributes_description = [
            {
                "name": "voltage",
                "dtype": "float",
                "Unit": "V",
                "fget": "default_get",
            }
        ]
        attributes_description = json.dumps(attributes_description)

        # Process the messages
        device.test_process_attribute_self_description(attributes_description)

        assert "voltage" in device.get_attribute_list()

        device.test_add_fake_voltage_value(123.4)

        assert device.voltage == 123.4

        attributes_description_2 = [
            {
                "name": "voltage_2",
                "dtype": "float",
                "Unit": "V",
                "fget": "default_get",
            }
        ]
        attributes_description_2 = json.dumps(attributes_description_2)

        # Process the messages
        device.test_process_attribute_self_description(
            attributes_description_2
        )

        assert "voltage" not in device.get_attribute_list()

        assert "voltage_2" in device.get_attribute_list()


@patch("mcmax.mcmax.Client")
def testDynamicCommandCreation(mocker, deviceProxy):
    """Test device can send messages to MQTT broker"""

    class TestDev(McMaxTangoDs):
        @command(dtype_in=str)
        async def test_process_commands_self_description(self, string):
            msg = MqttMessage(payload=string, topic="test/notopic")
            self.process_commands_self_description(None, None, msg)

    with DeviceTestContext(
        TestDev,
        properties={
            "broker": "localhost",
            "username": "user",
            "password": "password",
            "mqtt_name": MQTT_NAME,
        },
        process=True,
    ) as device:

        commands_description = [
            {
                "name": "new_command",
            }
        ]
        commands_description = json.dumps(commands_description)

        # Process the messages
        device.test_process_commands_self_description(commands_description)

        assert "new_command" in device.get_command_list()

        device.new_command("test string input")

        device.test_process_commands_self_description(commands_description)

        commands_description_2 = [
            {
                "name": "new_command_2",
            }
        ]
        commands_description_2 = json.dumps(commands_description_2)

        # Process the second mesage
        device.test_process_commands_self_description(commands_description_2)

        assert "new_command" not in device.get_command_list()

        assert "new_command_2" in device.get_command_list()

        device.new_command_2("test string input")
