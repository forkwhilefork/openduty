from openduty.models import Incident

__author__ = 'deathowl'

import smtplib
from django.template.defaultfilters import truncatechars

class EmailNotifier:
    def __init__(self, config):
        self.__config = config
    def notify(self, notification):

        host = self.__config['host']
        port = self.__config['port']
        user = self.__config['user']
        password = self.__config['password']
        truncate_length = int(self.__config.get('max_subject_length', 100))
        FROM = self.__config['user']
        TO = [notification.user_to_notify.email]
        try:
            SUBJECT = "Openduty Incident Report - {0}".format(notification.incident.description)
        except:
            SUBJECT = notification.message
        if truncate_length:
            SUBJECT = truncatechars(SUBJECT, truncate_length)
        TEXT =  notification.message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP(host, int(port))
            if self.__config['tls']:
                server.starttls()
            server.ehlo()
            if user and password:
                server.login(user, password)
            server.sendmail(FROM, TO, message)
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"
