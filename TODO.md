###   Greenhouse temperature control project

## goal:  keep trees/plants alive through the winter by providing an environment with stable temperature

# Modules:

# config
- read/write configuration variables (temperature setpoint, Kp, Ki, Kd, cycle time)
- initially write config to file
- read from file
- stat file and report if mod time changed

## Devices

# LED
- led on/off
- test: blink led

# Lamp
- lamp on/off
- test: blink lamp

# heater
- heater on/off at power levels
- cycle power for time period
- bounds test power

# cleanup
- reset gpio, ...
- call superclass cleanup

## Sensors

# dht22
- read temperature
- retry on fail
- report temp (C and F), humidity
- test: show temperature

# ds18b20
- read temperature
- report temp (C and F)
- test: show temperature

# ISStreamer (graph)
- log values to Initial State Service
- temperature, humidity, setpoint temperature, outside temperature, (?) diff of setpoint vs temperature
- test: log test values

# plot
- store values for plot
- matplotlib to make graphs
- trigger for graph?

# logger
- use logzero for logging

# deamon
- config and start daemon

# main
- control temperature via pid control of heater

