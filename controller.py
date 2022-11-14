"""Greenhouse Temperature Controller"""


from simple_pid import PID

import config
import data_streamer
import heater
import sensor_dht22
import sensor_ds18b20

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


pid = PID(1.0, 0.0, 0.0, setpoint=60.0)
pid.output_limits = (0, 100)
pid.auto_mode = True
pid.proportional_on_measurement = False
pid.differetial_on_measurement = True

ctrl_config = config.Config(50, 1.876, 0.556, 2.6, 30)
pid.setpoint, pid.Kp, pid.Ki, pid.Kd, pid.sample_time = ctrl_config.read_config()

ds_sensor = sensor_ds18b20.SensorDS18B20()

dht_sensor = sensor_dht22.SensorDHT22()

gh_heater = heater.Heater()

streamer = data_streamer.DataStreamer(
    temp=45.0, goal_temp=68.0, out_temp=45.0, hum=90.0, pwr=0
)


def cleanup():
    """Close resources."""
    streamer.cleanup()
    heater.cleanup()
    dht_sensor.cleanup()


def test():
    """Test controller."""
    cleanup()


def main():
    """Controller main loop"""
    while True:
        try:
            if ctrl_config.config_modified():
                (
                    pid.setpoint,
                    pid.Kp,
                    pid.Ki,
                    pid.Kd,
                    pid.sample_time,
                ) = ctrl_config.read_config()

            out_temp = ds_sensor.read_temp()
            temp, hum = dht_sensor.read_temp()

            pwr = pid(temp)
            gh_heater.heater_cycle(pwr, cycle_time=pid.sample_time)

            streamer.load_data(
                temp=temp, goal_temp=pid.setpoint, out_temp=out_temp, hum=hum, pwr=pwr
            )
            streamer.send_data()
        except KeyboardInterrupt:
            cleanup()
    cleanup()


if __name__ == "__main__":
    main()
