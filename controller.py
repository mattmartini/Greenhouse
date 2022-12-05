"""Greenhouse Temperature Controller"""


import signal

from simple_pid import PID

import config
import data_streamer
import heater
import sensor_ds18b20
import sensor_shtc3
import mailer

# import sensor_dht22

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.1.0"


pid = PID(1.0, 0.0, 0.0, setpoint=60.0)
pid.output_limits = (0, 100)
pid.auto_mode = True
pid.proportional_on_measurement = False
pid.differetial_on_measurement = True

ctrl_config = config.Config(40, 1.876, 0.125, 0.6, 25)
pid.setpoint, pid.Kp, pid.Ki, pid.Kd, pid.sample_time = ctrl_config.read_config()

ds_sensor = sensor_ds18b20.SensorDS18B20()

# dht_sensor = sensor_dht22.SensorDHT22()

sht_sensor = sensor_shtc3.SensorSHTC3()

gh_heater = heater.Heater()

streamer = data_streamer.DataStreamer(
    temp=45.0, goal_temp=40.0, out_temp=45.0, hum=90.0, pwr=0
)


def cleanup():
    """Close resources."""
    streamer.cleanup()
    heater.cleanup()
    # dht_sensor.cleanup()
    sht_sensor.cleanup()
    print("Exiting Greenhouse Temperature Control", flush=True)


class SignalHandler:
    """Gracefully handle a HUP signal to print data"""

    hupped_now = False
    usr1_now = False
    usr2_now = False

    def __init__(self):
        """Initialize signal handler."""
        signal.signal(signal.SIGHUP, self.hup_handler)
        signal.signal(signal.SIGUSR1, self.usr1_handler)
        signal.signal(signal.SIGUSR2, self.usr2_handler)

    def hup_handler(self, *args):
        """flag the hup"""
        self.hupped_now = True

    def usr1_handler(self, *args):
        """flag the usr1 signal"""
        self.usr1_now = True

    def usr2_handler(self, *args):
        """flag the usr2 signal"""
        self.usr2_now = True


def toggler(value):
    "Toggle the input true/false"
    if value is True:
        return False
    elif value is False:
        return True
    else:
        return value


def test():
    """Test controller."""
    cleanup()


def main():
    """Controller main loop"""
    print("Starting Greenhouse Temperature Control", flush=True)
    signal_test = SignalHandler()
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
                print(ctrl_config, flush=True)

            out_temp = ds_sensor.read_temp()
            temp, hum = sht_sensor.read_temp()

            pwr = pid(temp)
            gh_heater.heater_cycle(pwr, cycle_time=pid.sample_time)

            streamer.load_data(
                temp=temp, goal_temp=pid.setpoint, out_temp=out_temp, hum=hum, pwr=pwr
            )
            streamer.send_data()

            if signal_test.hupped_now:
                print(ctrl_config, flush=True)
                print("\n", flush=True)
                print(streamer, flush=True)
                signal_test.hupped_now = False

            if signal_test.usr1_now:
                pid.proportional_on_measurement = toggler(
                    pid.proportional_on_measurement
                )
                print(
                    f"proportional_on_measurement toggled to {pid.proportional_on_measurement}",
                    flush=True,
                )
                signal_test.usr1_now = False

            if signal_test.usr2_now:
                pid.differetial_on_measurement = toggler(pid.differetial_on_measurement)
                print(
                    f"differential_on_measurement toggled to {pid.differetial_on_measurement}",
                    flush=True,
                )
                signal_test.usr2_now = False

            if temp < 35.0:
                subject = "Greenhouse Low Temperature Alert"
                message = f"The Greenhouse temperature is {temp:3.3f} F!"
                mail = mailer.Mailer(subject, message)
                mail.send()

        except KeyboardInterrupt:
            cleanup()
    cleanup()


if __name__ == "__main__":
    main()
