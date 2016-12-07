#!/usr/bin/env python


DATABASE_CREDENTIALS = {
        'NAME': 'wyounas$school_census',
        'USER': 'wyounas',
        'PASSWORD': 'schoolcensus',
        'HOST': 'wyounas.mysql.pythonanywhere-services.com',
        'PORT': '3306'}

smtp_host = 'mail.vitalinteraction.com'
from_email = 'vitalinteraction@gmail.com'
email_password = 'somenewpassword'
to_email_address = 'u.leo86@gmail.com'
smtp_server= 'smtp.gmail.com'
smtp_port = 587

NULLS = ['', None, 'NULL', 'null', 'nill', 'Null', 'NUL', 0, '0', 'none', 'None']
HOST_NAME = 'LocalDevStack'
SUPPORT_EMAIL_ID = 'vitalinteraction@gmail.com'
ENVIRONMENT = HOST_NAME.upper()
default_email_subject = '[%s] Error occurred while running on Scripts' % (HOST_NAME)
BASE_PATH = '/home/wyounas/punjab-school-census-analysis/school-census/'
FILES_PATH = BASE_PATH + 'files'
LOG_FILE = 'application_log.log'
log_file_name = '%s/logs/%s' % (BASE_PATH, LOG_FILE)
