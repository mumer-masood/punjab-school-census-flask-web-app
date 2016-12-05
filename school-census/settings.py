#!/usr/bin/env python


DATABASE_CREDENTIALS = {
        'NAME': 'school_census',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3310'}

smtp_host = "mail.vitalinteraction.com"
from_email = "vitalinteraction@gmail.com"
email_password = "somenewpassword"
to_email_address = "u.leo86@gmail.com"
smtp_server= "smtp.gmail.com"
smtp_port = 587

NULLS = ['', None, 'NULL', 'null', 'nill', 'Null', 'NUL', 0, '0', 'none', "None"]
HOST_NAME = 'LocalDevStack'
SUPPORT_EMAIL_ID = 'vitalinteraction@gmail.com'
ENVIRONMENT = HOST_NAME.upper()
default_email_subject = "[%s] Error occurred while running on Scripts" % (HOST_NAME)

FILES_PATH = '/home/bravo/PycharmProjects/school-census/files/'
log_name = 'application_log.log'
log_file_name = "/home/bravo/PycharmProjects/school-census/" + log_name

