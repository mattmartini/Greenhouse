"""Temperature Sensor (DS18B20)."""

import glob
import os
import time

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


class SensorDS18B20:
    """DS18B20 Temperature Sensor."""

    def __init__(self, scale="f"):
        """Initialize sensor."""
        self.scale = scale

        # These tow lines mount the device:
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")

        self.base_dir = "/sys/bus/w1/devices/"
        # Get all the filenames begin with 28 in the path base_dir.
        self.device_folder = glob.glob(self.base_dir + "28*")[0]
        self.device_file = self.device_folder + "/w1_slave"

    def read_rom(self):
        """Get name of device."""
        name_file = self.device_folder + "/name"
        with open(name_file, "r", encoding="utf-8") as file:
            return file.readline()

    def read_temp_raw(self):
        """Read raw temperature."""
        with open(self.device_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            file.close()
            if bool(lines):
                return lines
            else:
                return ["\n","\n"]

    def convert_c_to_f(self, temp_c):
        """Convert temperature from C to F"""
        return temp_c * 9.0 / 5.0 + 32.0

    def read_temp(self):
        """Read temperature with retry."""
        lines = self.read_temp_raw()
        # Analyze if the last 3 characters are 'YES'.
        count = 0
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self.read_temp_raw()
            count =+ 1
            if (count == 10):
                print("WARNING: Failed to read temperature on ds1b20 after 10 attempts.")
                return -99
        # Find the index of 't=' in a string.
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            if self.scale == "f":
                return self.convert_c_to_f(temp_c)
            return temp_c


def test():
    """Read temperature from DS18B20 via parsing"""

    my_sensor = SensorDS18B20()

    print(f" rom: {my_sensor.read_rom()}")
    print(f"temp: {my_sensor.read_temp():3.3f} F")

    my_c_sensor = SensorDS18B20(scale="c")

    print(f"temp: {my_c_sensor.read_temp():3.3f} C")


if __name__ == "__main__":
    test()
