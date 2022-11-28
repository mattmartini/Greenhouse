"""Temperature Sensor (DHT22)."""

import time

import adafruit_dht
import board

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


class SensorDHT22:
    """DHT22 Temperature Sensor."""

    def __init__(self, pin="D18", scale="f"):
        """Initialize sensor."""
        self.pin = pin
        self.scale = scale
        # TODO find out how to pass pin to board
        self.dht_sensor = adafruit_dht.DHT22(board.D18, use_pulseio=True)

    def convert_c_to_f(self, temp_c):
        """Convert temperature from C to F"""
        return temp_c * 9.0 / 5.0 + 32.0

    def read_temp(self):
        """Read temperature with retry."""
        for _ in range(5):
            try:
                temp_c = self.dht_sensor.temperature
                humidity = self.dht_sensor.humidity
                break
            except RuntimeError:
                time.sleep(0.5)
                continue
        if self.scale == "f":
            return self.convert_c_to_f(temp_c), humidity
        return temp_c, humidity

    def cleanup(self):
        """Close resources."""
        self.dht_sensor.exit()


def test():
    """Read temperature from DHT22 sensor."""

    my_sensor = SensorDHT22()
    tempf, humf = my_sensor.read_temp()
    print(f"temp: {tempf:3.3f} F")
    print(f" hum: {humf:3.3f} %")
    my_sensor.cleanup()

    time.sleep(3)

    my_c_sensor = SensorDHT22(scale="c")
    tempc, humc = my_c_sensor.read_temp()
    print(f"temp: {tempc:3.3f} C")
    print(f" hum: {humc:3.3f} %")
    my_c_sensor.cleanup()


if __name__ == "__main__":
    test()
