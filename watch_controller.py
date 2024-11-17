#!/usr/bin/python
"""Watch processes to insure controller is running"""

import subprocess

# import psutil
import mailer

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "0.1.0"


CMD = "/usr/local/bin/svok"
ARGS = "/service/greenhouse"

CONTROLLER_PID = "/run/controller.pid"


# def read_pid():
#     """Get the pid of the controller"""
#     pid_file = CONTROLLER_PID
#     with open(pid_file, "r", encoding="utf-8") as file:
#         return file.readline()


def main():
    """Check if controller is running, email alert if not"""
    # pid = int(read_pid())
    # pids = psutil.pids()

    # if (pid not in pids):
    if subprocess.run([CMD, ARGS], check=False).returncode:
        subject = "Greenhouse Controller DOWN!!"
        message = "The Greenhouse Controller process is not running.  Restart!"
        msg = mailer.Mailer(subject, message)
        msg.send()
        msg.cleanup()


if __name__ == "__main__":
    main()
