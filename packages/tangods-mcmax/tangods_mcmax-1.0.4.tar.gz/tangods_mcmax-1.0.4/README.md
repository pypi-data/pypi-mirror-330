# Tango Device Server for the MC-MAX project

This tango device server connects to an mqtt broker using the paho-mqtt library
and upon success reads the esp-32 self description topic, and starts a tango
device with dynamic attributes and commands.

## Properties

Name | Description
---- | ----
`broker` | A string, URI of the mqtt broker
`username` | The username for the mqtt broker connection
`password` | The password for the mqtt broker connection
`mqtt_name` | The name of the microcontroller in the mqtt topic tree. Usually it's the hostname of the microcontroller (without domain).
