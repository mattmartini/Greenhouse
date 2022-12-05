###   Greenhouse Temperature Control Project

## Goal:
Keep trees/plants alive through the winter by providing an environment
with stable temperature

## Equipment
- Raspberry pi 3 Model B
- Temperature Sensor SHTC3
- Temperature Sensor DHT22 - retired in favor of SHTC3
- Temperature Sensor DS18B20
- 30A Relay
- Portable Heater

## Methodology

Use temperature sensors (dht22 & ds18b20) to measure inside temperature
and humidity, and outside temperature (respectivly). The shtc3 sensor
replaces the dht22.  It is more accurate, and more importantly uses
IC2 communication which is more reliable.

Use a tuned PID controller to run a heater inside the greenhouse.
Variable power settings (needed for PID) are aproximated via
timeslicing.

Temperature setpoint, PID K values, and Cycle Time kept in a config
file. Changes to config file trigger reloading of config variables.
Allows for on-the-fly tweeking of parameters.

Temperature, Humidity, and Power data are sent to initial state
for graphing.

Modules contain thier own tests. Call a module directly to run tests.

### Note
See the wiki for graphs of the system in use, plus descriptions of the implementation process.
