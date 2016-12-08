"""

"""
import logging
import re
import traceback
import urllib2
from collections import deque

from bs4 import BeautifulSoup
from sqlalchemy import sql

import constants
import settings
from models import school
from models import base_model

LOGGER = logging.getLogger(__file__)


class Scraper:
    """

    """
    def __init__(self, *args, **kwargs):
        """"""
        self.max_attempts = kwargs.get('max_attempts', 3)
        self.url = kwargs['url']
        self.css_classes = kwargs.get('css_classes')
        self.tags = kwargs.get('tags')
        self.fields_to_scrape = kwargs['fields_to_scrape']
        self.scraped_fields_data = {}

    def get_http_data(self):
        """"""
        response = None
        for attempt in range(0, self.max_attempts):
            try:
                http_resp = urllib2.urlopen(self.url, timeout=60)
            except Exception:
                err_msg = traceback.format_exc()
                LOGGER.debug('Error occured: %s', err_msg)
                if attempt == self.max_attempts:
                    raise
            else:
                response = http_resp.read()
                http_resp.close()
                LOGGER.debug('Request response Data: %s', response)
                break
        return response

    def scrape(self):
        """"""
        http_data = self.get_http_data()
        if http_data is not None:
            soup = BeautifulSoup(http_data, 'html.parser')
            for field in self.fields_to_scrape:
                field_data = soup.find('b', text=re.compile(
                    field['field_to_scrape'], re.IGNORECASE))
                field_data = re.findall('\d+', field_data.text)
                field_value = field_data.pop()
                field_value = int(field_value)
                self.scraped_fields_data[field['db_field']] = field_value
        else:
            err_msg = ('Did not get data for record from school portal '
                       'server: %s', self.url)
            LOGGER.info(err_msg)
            raise Exception(err_msg)



class DataUpdator:
    """"""
    fetched_records = deque()
    total_fetched_records = 0
    total_updated_records = 0

    def __init__(self, *args, **kwargs):
        """"""


class DataUpdateManager:
    """"""
    RECORDS_TO_UPDATE = 5000
    MAX_RECORDS_PER_THREAD = 500
    fetched_records = deque()
    total_fetched_records = 0
    total_updated_records = 0

    # def __init__(self, *args, **kwargs):
    #     """"""

    def process(self):
        """"""
        try:
            self.fetch_records()
            self.update_records()
        except Exception:
            err_msg = traceback.format_exc()
            LOGGER.critical('%s\n%s' % ('Error detail:', err_msg))

    def fetch_records(self):
        """"""
        query = school.School.query
        query = query.filter(school.School.updated == 0,
                             school.School.update_tries < 3).limit(
            DataUpdateManager.RECORDS_TO_UPDATE)
        DataUpdateManager.fetched_records = query.all()
        self.total_fetched_records = len(self.fetched_records)

    def update_record(self, record):
        """"""
        updated = False
        url = constants.SCRAPE_WEB_URL % record.emiscode
        scraper = Scraper(url=url, fields_to_scrape=constants.SCRAPE_FIELDS)
        scraper.scrape()
        for field in constants.SCRAPE_FIELDS:
            model_class = base_model.get_class_by_tablename(
                field['model_class_name'])
            db_record = model_class.get_by_id(record.emiscode)
            field_value = scraper.scraped_fields_data[field['db_field']]
            if (type(model_class.__table__.c[field['db_field']].type) == sql.sqltypes.Integer
                and scraper.scraped_fields_data[field['db_field']] not in settings.NULLS):
                field_value = int(field_value)
                updated = db_record.update(**{field['db_field']: field_value})
            elif scraper.scraped_fields_data[field['db_field']] not in settings.NULLS:
                updated = db_record.update(**{field['db_field']: field_value})

        return updated


    def update_records(self):
        """"""
        index = 0
        updated = None
        while len(self.fetched_records):
            index += 1
            LOGGER.info('| Processing (%d of %d) appointment', index,
                        self.total_fetched_records)
            record = self.fetched_records.pop()
            try:
                updated = self.update_record(record)
            except Exception:
                err_msg = traceback.format_exc()
                LOGGER.debug('Error detail:%s', err_msg)
            school_obj = school.School.get_by_id(record.emiscode)
            if updated:
                data = {'updated': 1,
                        'update_tries': school_obj.update_tries + 1}
                school_obj.update(**data)
            else:
                data = {'update_tries': school_obj.update_tries + 1}
                school_obj.update(**data)
            base_model.QueryMixin.session.commit()



    # def run(self):
    #     """"""

    def clean_up(self):
        """"""
        pass
