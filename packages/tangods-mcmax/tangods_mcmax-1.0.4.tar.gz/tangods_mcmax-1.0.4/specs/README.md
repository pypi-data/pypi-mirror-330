# Specifications for the MC-MAX project

The MC-MAX project encompasses four components:

1. Microcontroller firmware
2. Tango device server
3. A data formatting specification to allow the two system above to communicate, described [further down](#mqtt-data-exchange-format) in this document.
4. CI/CD toolchain (gitlab CI + ansible) to monitor the firmware and deploy updates.

## Microcontroller firmware

The microcontroller must belong to Espressif's ESP32 family.

The firmware must be compiled using the [esp-idf](https://github.com/espressif/esp-idf) toolchain. This is because it simplify devOps.

The Microcontroller must have the following features:
1. Use OTA firmware update: it should be possible to update the microcontroller remotely.
2. Use MQTT protocol: simple and easy, the microcontroller should describe its own features and firmware.
3. Self describe its features according to the [MQTT data exchange specification](#mqtt-data-exchange-format).
4. [*Not confirmed*] display a web page for configuration. In any case, the MQTT broker address must be configured somehow.

## Tango DS

There should be only **one** tango device server class, capable of adapting to all the different firmwares.

One tango device connects to one microcontroller.

It must have a tango property for the microcontroller hostname, to find the appropriate device in the MQTT tree.

It must populate attributes and commands dynamically, by reading the microcontroller self description through MQTT.

## MQTT data exchange specification

The microcontroller must advertise the following:
1. Firmware flavor (a name, example "Relay controller").
2. Firmware version. Must be the same as the output of `git-describe`.
3. Self description. A JSON formatted dictionary having all the tango goodies: which tango attributes, which tango commands and so on.
4. Somewhere to publish the data.
5. Somewhere to listen for data.

Here is how the MQTT topic tree should look like:

```
mc_max
└─ <hostname, without domain>
   ├─ firmware_name: str
   ├─ firmware_version: str
   ├─ tango_attributes: str (list of valid keyword dictionaries to create attributes, JSON formatted)
   ├─ tango_commands: str (list of valid keyword dictionaries to create commands, JSON formatted)
   ├─ mc_output
   │  ├─ variable_1: str
   │  ├─ variable_2: str
   │  ├─ ...
   │  └─ variable_n: str
   ├─ mc_input
   │  ├─ variable_1: str
   │  ├─ variable_2: str
   │  ├─ ...
   │  └─ variable_n: str
   └─ command
      ├─ command_1: str
      ├─ command_2: str
      ├─ ...
      └─ command_n: str
```

So to have a complete example:

`mc_max/mydevice/mc_output/voltage` could contain useful data that must be translated to a tango attribute; while `mc_max/mydevice/mc_input/voltage` could be used as a setpoint for a controlled process variable.

For a command, there is a list called `command`. Commands always have a string as `dtype_in`. Exaple writing `"1"` into `mc_max/mydevice/command/enable_voltage` could tell the microcontroller to perform a specific action such as switching voltage on.

This feature could be used with more complex parameters, to pass data together with a command. Example: writing `'{"time": "1s", "voltage": "2V"}'` into the topic `mc_max/mydevice/command/pulse_voltage` could perform the complex action of pulsing the voltage on the microcontroller.