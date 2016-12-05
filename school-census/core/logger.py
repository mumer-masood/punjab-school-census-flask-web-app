"""
In this logger file we are overriding the default logging behavior of logger
levels.
"""
#===============================================================================
# Python imports
#===============================================================================
import logging
import logging.handlers
import logging.config
import os
from datetime import datetime

from core import emailer
from settings import smtp_port
from settings import from_email
from settings import smtp_server
from settings import log_file_name
from settings import email_password
from settings import default_email_subject

LOGGER = logging.getLogger(os.path.basename(__file__))


class RotatingHandler(logging.handlers.RotatingFileHandler):

    """ We are creating a file and set it to append mode """

    def _open(self):
        if not os.path.exists(self.baseFilename):
            f = open(self.baseFilename, 'w')
            try:
                # raises exception if file is created on filesystems which
                # don't support modes such as fat32 or exfat
                os.chmod(self.baseFilename, 0o644)
            except OSError as e:
                LOGGER.warn('Could not set file mode: %s', e)
            f.close()
        file_obj = open(self.baseFilename, 'a')
        return file_obj


class Logger(logging.Logger):
    """ We are creating a logger to define the customize behavior of 'error' and
        'critical' level """
    # ===========================================================================
    # Static data member
    run_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    host = smtp_server
    port = smtp_port
    username = from_email
    password = email_password

    # ===========================================================================
    # Overriding logging level called critical. This level sends email only
    # ===========================================================================

    def critical(self, message, subject=default_email_subject, *args, **kwargs):
        """ We are overriding this level so that we may use it to log
            errors via email """
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, message, args, **kwargs)
            try:
                emailer.send_email(message=message)
            except Exception as error:
                msg = ("Email Sending Failed: Not able to send Error email," +
                       " Internet not accessible while sending email, Error: %s"
                       + "\n\n Actual Message: %s") % (error, message)
                LOGGER.debug(msg)

    logging.Logger.critical = critical  # assigning a call back function
    # ===========================================================================
    # logger is static data member
    # ===========================================================================
    logger = logging.getLogger()

    @staticmethod
    def set_up_logger(**args):
        """ We are setting the logger levels to log at various places"""
        Logger.logger.setLevel(logging.CRITICAL)
        Logger.logger.setLevel(logging.ERROR)
        Logger.logger.setLevel(logging.DEBUG)

        console_handler_added_already = False
        file_hadler_added_already = False
        for added_handler in Logger.logger.handlers:
            if isinstance(added_handler, RotatingHandler):
                file_hadler_added_already = True
            if isinstance(added_handler, logging.StreamHandler):
                console_handler_added_already = True

        if not console_handler_added_already:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            Logger.logger.addHandler(console)

        if not file_hadler_added_already:
            # create a file handler to log detailed messages to a file
            file_handler = RotatingHandler(log_file_name)
            file_format = '%(asctime)s %(levelname)6s %(name)s : %(message)s'
            file_handler.setFormatter(logging.Formatter(file_format))
            file_handler.setLevel(logging.DEBUG)
            file_handler.propogate = False
            Logger.logger.addHandler(file_handler)


def setup_logging(**args):
    """ Here we are calling the setup method of logger """
    Logger.set_up_logger(**args)
