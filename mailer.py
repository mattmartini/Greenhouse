"""Send status messages via email"""


import signal

import smtplib


__author__ = "Matt Martini"
__email__ = "matt.martini@imaginarywave.com"
__version__ = "0.1.0"


class Mailer:
    """Send email (and SMS via email) on alert condition."""

    def __init__(self, subject, message):
        """Initialize streamer."""
        self.subject = subject
        self.message = message
        self.header = ""
        self.silence = False
        self.sender = "pi@greenhouse.local"
        self.receivers = [
            "receiver@example.com"
        ]

    def send(self):
        """Send prepaired message via smtp"""
        self.header = """From: Greenhouse Controller <pi@greenhouse.local>
To: <receiver@example.com>
"""
        self.header = self.header + "Subject: " + self.subject + "\n\n"
        self.message = self.header + self.message
        if not self.silence:
            try:
                smtp_obj = smtplib.SMTP("cathal.local")
                smtp_obj.sendmail(self.sender, self.receivers, self.message)
                print("Successfully sent email")
                self.stall()
            except smtplib.SMTPException:
                print("Error: unable to send email")

    def stall_handler(self, *args):
        """Reset silence flag afer alarm goes off."""
        self.silence = False

    def stall(self):
        """Wait 10 minutes before sending another email."""
        self.silence = True
        signal.signal(signal.SIGALRM, self.stall_handler)
        signal.alarm(600)

    def cleanup(self):
        """Cleanup alarm."""
        signal.alarm(0)
        self.silence = False

    def __del__(self):
        """Ensure cleanup."""
        self.cleanup()


def test():
    """Test config methods."""
    subject = "Alert Test"
    message = "You can ignore this test message. But you should only get one."
    msg = Mailer(subject, message)
    print("DEBUG: Sending message, it should send.")
    print(msg.message)
    msg.send()

    msg.subject = "Alert Silence Test"
    msg.message = "You should not receive this message. It should be silenced."

    print("DEBUG: Attempting second message during silence period, should not send.")
    msg.send()
    print("DEBUG: This line should print even as the second email was not sent.")

    msg.cleanup()


if __name__ == "__main__":
    test()
