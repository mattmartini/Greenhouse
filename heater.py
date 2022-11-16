"""Turn heater on and off"""

import time

from RPi import GPIO

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


class Heater:
    """Heater with variable power output aproximated via time slicing."""

    def __init__(self, pin=21):
        """Initialize heater."""
        self.pin = pin

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        """Turn the heater on."""
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        """Turn the heaterLED off."""
        GPIO.output(self.pin, GPIO.LOW)

    def heater_cycle(self, power, cycle_time=10):
        """Use percentage of time cycle to aproximate variable power."""
        if (power < 0) or (power > 100):
            power = 0

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
        GPIO.cleanup()


def test():
    """Test heater."""

    my_heater = Heater()

    for _ in range(3):
        my_heater.turn_on()
        time.sleep(5.0)
        my_heater.turn_off()
        time.sleep(2.0)

    my_heater.heater_cycle(20, cycle_time=15)
    my_heater.heater_cycle(80)

    my_heater.cleanup()


if __name__ == "__main__":
    test()
