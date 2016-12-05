import logging
import os
import sys
import traceback

import argparse
#===============================================================================
# Changing the current working directory, that is set the current working
# directory to the directory of this file.

FILE_PATH = os.path.realpath(__file__)
DIR_PATH, _ = os.path.split(FILE_PATH)
PATH = os.path.abspath(os.path.join(DIR_PATH, '..', '..'))
sys.path.append(PATH)
#===============================================================================
import constants
from core import logger
from core import cleanser
from core import data_updator
from db import db_session

logger.setup_logging()
LOGGER = logging.getLogger(__file__)


class AppManager():

    """AfterAppointmentLoaderManager loads after appointments for
    patients based on criteria provided through parameters to constructor
    """

    def __init__(self, **kwargs):
        """"""
        self.parse_data_option = None
        self.update_data_option = None
        self.parse_data_option = kwargs[constants.PARSE_DATA_KEY]
        self.update_data_option = kwargs[constants.UPDATE_DATA_KEY]

    def run(self):
        """See base class"""
        action_class = self.get_action_class()
        action_obj = action_class()
        action_obj.process()

    def get_action_class(self):
        """

        :return:
        """
        action_class = None
        if self.parse_data_option:
            action_class = cleanser.Cleanser
        if self.update_data_option:
            action_class = data_updator.DataUpdateManager

        return action_class


def main():
    parser = argparse.ArgumentParser(description='Loads data of excel files also scafiles')

    parser.add_argument('-p', '--parse',
                        action='store_true',
                        dest=constants.PARSE_DATA_KEY,
                        default=False,
                        help='parse file(s) data and load into database.')
    parser.add_argument('-u', '--update',
                        action='store_true',
                        dest=constants.UPDATE_DATA_KEY,
                        default=False,
                        help='Scrape data and update the records in database.')

    options = parser.parse_args()
    if not options.parse_data and not options.update_data:
        raise Exception('There is no command line option given, please give '
                        'one. There are two options')

    try:
        manager = AppManager(**vars(options))
        manager.run()
    except:
        subject = 'After Appointment Loader: Unable to Process'
        msg = 'Given options= %s \n' % (options)
        msg += 'Detail error= %s' % (traceback.format_exc())
        LOGGER.critical(msg, subject=subject)
    finally:
        db_session.close()


if __name__ == '__main__':
    main()