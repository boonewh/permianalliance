"""Flask-Mail connection with verified TLS and a bounded network timeout."""
import smtplib
import ssl

import certifi
from flask import current_app
from flask_mail import Connection, Mail


class VerifiedConnection(Connection):
    def configure_host(self):
        context = ssl.create_default_context(cafile=certifi.where())
        host = smtplib.SMTP(self.mail.server, self.mail.port, timeout=15)
        try:
            host.starttls(context=context)
            if self.mail.username and self.mail.password:
                host.login(self.mail.username, self.mail.password)
        except Exception:
            host.close()
            raise
        return host


class VerifiedMail(Mail):
    def connect(self):
        app = self.app or current_app
        return VerifiedConnection(app.extensions['mail'])
