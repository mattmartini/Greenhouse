"""Watch processes to insure controller is running"""

import subprocess

import mailer

__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "0.1.0"


CMD = "/usr/local/bin/svok"
ARGS = "/service/greenhouse"


def main():
    """Check if controller is running, email alert if not"""

    if subprocess.run([CMD, ARGS]).returncode:
        subject = "Greenhouse Controller DOWN!!"
        message = "The Greenhouse Controller process is not running.  Restart!"
        msg = mailer.Mailer(subject, message)
        msg.send()
        msg.cleanup()


if __name__ == "__main__":
    main()
