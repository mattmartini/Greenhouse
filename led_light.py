"""Turn LED on and off."""

import time

import board
import digitalio

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "0.1.0"


class LED:
    """Class for a LED light."""

    def __init__(self, pin="D26"):
        """Initialize LED light."""
        self.pin = pin
        # TODO find out how to pass pin to board
        self.led = digitalio.DigitalInOut(board.D26)
        self.led.direction = digitalio.Direction.OUTPUT

    def turn_on(self):
        """Turn the LED on."""
        self.led.value = True

    def turn_off(self):
        """Turn the LED off."""
        self.led.value = False

    def cleanup(self):
        """Close resources."""
        self.turn_off()
        self.led.deinit()


def test():
    """Test LED blink."""
    my_led = LED()

    for _ in range(10):
        my_led.turn_on()
        time.sleep(1.0)
        my_led.turn_off()
        time.sleep(1.0)

    my_led.cleanup()


if __name__ == "__main__":
    test()
