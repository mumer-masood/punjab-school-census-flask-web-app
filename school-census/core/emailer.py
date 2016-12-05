from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import logging
from smtplib import SMTP
from smtplib import SMTPDataError
import traceback

from settings import (to_email_address, from_email, smtp_server,
                      email_password, default_email_subject)

LOGGER = logging.getLogger(__file__)

def send_email(message="Mayday, mayday. Something went wrong "
                       "while running Scripts.", subject=default_email_subject,
               mail_to = to_email_address):

    try:
        data = []
        if mail_to.find(',') != -1:
            mail_to = mail_to.split(",")

        mail_from = from_email
        msg_en = message
        smtp_serv = SMTP(smtp_server, 587)
        smtp_serv.ehlo()
        smtp_serv.starttls()
        smtp_serv.ehlo()
        #if server requires authorization you must provide login and password
        smtp_serv.login(mail_from, email_password)
        date_ = formatdate(localtime = True)
        msg = MIMEMultipart()
        msg['From'] = mail_from
        if type(mail_to) == list and len(mail_to) > 1:
            msg['To'] = COMMASPACE.join(mail_to)
        else:
            msg['To'] = mail_to
        msg['Date'] = date_
        msg['Subject'] = subject
        msg.attach(MIMEText(msg_en))

        smtp_serv.sendmail(mail_from, mail_to, msg.as_string())
        smtp_serv.quit()

    except SMTPDataError:
        LOGGER.critical('Unable to send email. Exception details: \n%s', traceback.format_exc())
