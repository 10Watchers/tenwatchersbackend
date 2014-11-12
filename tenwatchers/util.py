import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
import uuid
import os
from flask import current_app

from twilio.rest import TwilioRestClient


account_sid = 'ACcdea1ecd57653e325bdb0d6a68128ea8'
auth_token = '22be35f15b29770ae254c54bbe11c1c3'
client = TwilioRestClient(account_sid, auth_token)

WHITELIST = [
    '+358504361615',
    '+16024323789'
]


def get_twilio_phone():
    return '+14428881219'


def send_sms(to_user, message):
    if to_user in WHITELIST:
        current_app.logger.info(
            "Sending SMS with PIN {0} to User {1}".format(message, to_user))
        message = client.messages.create(
            to=to_user,
            from_=get_twilio_phone(),
            body='{0}'.format(message)
        )


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')


def create_path_if_not_exist(path_and_file):
    path, _ = os.path.split(path_and_file)
    if not os.path.exists(path):
        os.makedirs(path)
    return path_and_file


def configure_logging(app):
        # Log to file
    if not app.debug:
        if app.config['ERROR_TO_FILE']:
            error_log_name = app.config['ERROR_LOG_NAME']
            file_handler = TimedRotatingFileHandler(
                filename=create_path_if_not_exist(error_log_name),
                when='d')
            file_handler.setFormatter(Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
            ))
            app.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info('Tenwatchers startup')
