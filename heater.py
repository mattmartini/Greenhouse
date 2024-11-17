"""Turn heater on and off"""

import time

from RPi import GPIO

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


class Heater:
    """Heater with variable power output aproximated via time slicing."""

    def __init__(self, pin=21, sw_pin=20):
        """Initialize heater."""
        self.pin = pin
        self.sw_pin = sw_pin

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setup(self.sw_pin, GPIO.OUT)
        # initialize heater to off
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.output(self.sw_pin, GPIO.LOW)

    def turn_on(self):
        """Turn the heater on."""
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        """Turn the heater off."""
        GPIO.output(self.pin, GPIO.LOW)

    def mode_half(self):
        """Switch the heater to Half Power mode."""
        GPIO.output(self.sw_pin, GPIO.LOW)
        # TODO check polarity

    def mode_full(self):
        """Turn the heater to Full Power mode."""
        GPIO.output(self.sw_pin, GPIO.HIGH)

    def heater_cycle(self, power, cycle_time=25):
        """Use percentage of time cycle to aproximate variable power.
        New heater has two power modes Half (750W) and Full (1500W)
        In order to have a more natural response we use a second relay
        to control which mode the heat utilizes. For computed power
        less than 50%, Half power mode for twice the duration and
        more than 50%, Full power mode for normal duration.
        So Half power for 100% cycle is the transition to Full power
        for 50% cycle.
        """
        if power < 0:
            power = 0
        elif power > 100:
            power = 100

        if power < 50:
            self.mode_half()
            power = power * 2
        else:
            self.mode_full()

        on_time = cycle_time * power / 100
        off_time = cycle_time * (100 - power) / 100

        if power > 0:
            self.turn_on()
            time.sleep(on_time)
        if power < 100:
            self.turn_off()
            time.sleep(off_time)

    def cleanup(self):
        """Close resources."""
        self.turn_off()
        self.mode_half()
        GPIO.cleanup()


def test():
    """Test heater."""

    my_heater = Heater()

    # for _ in range(3):
    #     my_heater.turn_on()
    #     time.sleep(5.0)
    #     my_heater.turn_off()
    #     time.sleep(2.0)

    my_heater.heater_cycle(30, cycle_time=30)
    my_heater.heater_cycle(60, cycle_time=30)
    my_heater.heater_cycle(20, cycle_time=30)

    my_heater.cleanup()


if __name__ == "__main__":
    test()
