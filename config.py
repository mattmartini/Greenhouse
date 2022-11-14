"""Keep config vars in a file.  Read/write/check if modified."""

import os

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "1.0.0"


DEFAULTCONFIGFILE = "/home/pi/greenhouse.conf"


class Config:
    """Class to hold configuration variables for PID."""

    def __init__(
        self,
        set_point,
        k_p,
        k_i,
        k_d,
        cycle_time,
        config_file=DEFAULTCONFIGFILE,
    ):
        """Initialize Config object."""
        self.set_point = set_point
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.cycle_time = cycle_time
        self.config_file = config_file
        self.mtime = 0
        self.create_config()

    def stat_config(self):
        """get the modification time of the config file"""
        if os.path.isfile(self.config_file):
            stat_info = os.stat(self.config_file)
            return stat_info.st_mtime
        return 0

    def create_config(self):
        """write the values to the config file"""
        if not os.path.isfile(self.config_file):
            with open(self.config_file, "w", encoding="utf-8") as file:
                file.write(
                    "%s,%s,%s,%s,%s"
                    % (self.set_point, self.k_p, self.k_i, self.k_d, self.cycle_time)
                )
        else:
            print("Warning: using existing configuration file", self.config_file)
        self.mtime = self.stat_config()

    def read_config(self):
        """read the values from the config file"""
        with open(self.config_file, "r", encoding="utf-8") as file:
            config = file.readline().split(",")
            self.set_point = float(config[0])
            self.k_p = float(config[1])
            self.k_i = float(config[2])
            self.k_d = float(config[3])
            self.cycle_time = float(config[4])
            return self.set_point, self.k_p, self.k_i, self.k_d, self.cycle_time

    def config_modified(self):
        """check if config file has been modified"""
        curr_time = self.stat_config()
        if curr_time > self.mtime:
            self.mtime = curr_time
            return True
        return False

    def __str__(self):
        """Pretty Print."""
        lines = ["Config:"]
        lines.append(f"Set Point={self.set_point}")
        lines.append(f"Cycle Time(s)={self.cycle_time}")
        lines.append(f"Kp={self.k_p}, Ki={self.k_i}, Kd={self.k_d}")
        lines.append(f"Config File={self.config_file}")
        return "\n".join(lines)


def test():
    """test config methods"""
    from pathlib import Path

    my_config = Config(75, 3.0, 0.1, 0.6, 10)

    print(my_config.read_config())

    print(my_config.stat_config())

    print(my_config)

    Path(my_config.config_file).touch()

    if my_config.config_modified():
        print("Configuration Modified!!")
        print(my_config.stat_config())
    else:
        print("Configuration Not Modified")


if __name__ == "__main__":
    test()
