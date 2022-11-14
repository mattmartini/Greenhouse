"""Stream temperature data to initialstate.com for graphing."""

import os

from ISStreamer.Streamer import Streamer

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


SENSOR_LOCATION_NAME = "Hothouse"
BUCKET_NAME = os.environ.get("BUCKET_NAME")
BUCKET_KEY = os.environ.get("BUCKET_KEY")
ACCESS_KEY = os.environ.get("ACCESS_KEY")


class DataStreamer:
    """Initial State Streamer"""

    def __init__(self, temp, goal_temp=40.0, out_temp=0, hum=0, pwr=0):
        """Initialize streamer."""
        self.temp = format(temp, ".2f")
        self.goal_temp = format(goal_temp, ".2f")
        self.out_temp = format(out_temp, ".2f")
        self.hum = format(hum, ".2f")
        self.pwr = format(pwr, ".2f")
        self.streamer = Streamer(
            bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY
        )

    def load_data(self, temp, goal_temp, out_temp, hum, pwr):
        """Load next data samples"""
        self.temp = format(temp, ".2f")
        self.goal_temp = format(goal_temp, ".2f")
        self.out_temp = format(out_temp, ".2f")
        self.hum = format(hum, ".2f")
        self.pwr = format(pwr, ".2f")

    def send_data(self):
        """Send data samples"""
        self.streamer.log(SENSOR_LOCATION_NAME + " Temperature(F)", self.temp)
        self.streamer.log(SENSOR_LOCATION_NAME + " GoalTemperature(F)", self.goal_temp)
        self.streamer.log(SENSOR_LOCATION_NAME + " Humidity(%)", self.hum)
        self.streamer.log(SENSOR_LOCATION_NAME + " Power(%)", self.pwr)
        self.streamer.log(
            SENSOR_LOCATION_NAME + " OutsideTemperature(F)", self.out_temp
        )
        self.streamer.flush()

    def cleanup(self):
        """Close resources."""
        self.streamer.flush()


def test():
    """Read temperature from DHT22 sensor."""

    import time

    my_streamer = DataStreamer(
        temp=45.0, goal_temp=68.0, out_temp=45.0, hum=90.0, pwr=0
    )
    my_streamer.send_data()
    time.sleep(10)
    my_streamer.load_data(temp=47.0, goal_temp=60.0, out_temp=40.0, hum=95.0, pwr=0)
    my_streamer.send_data()

    my_streamer.cleanup()


if __name__ == "__main__":
    test()
