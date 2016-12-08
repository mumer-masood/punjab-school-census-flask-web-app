import collections
import logging
import os
import traceback
from datetime import datetime

import xlrd
from fnmatch import fnmatch
from sqlalchemy import sql, DateTime

import constants
import settings
from core import excel_helper
from db import db_session
from models import school
from models import facilities

LOGGER = logging.getLogger(__file__)

class Cleanser(object):

    def __init__(self, *args, **kwargs):
        """"""
        self.file_path = ''
        self.delete_file = kwargs.get('delete_file', False)
        self.total_fetched_records = 0
        self.total_saved_records = 0
        self.records = collections.deque()
        self.status_code = constants.SUCCESS_CODE_LABEL
        self.start_time = None
        self.data_container = None
        self.db_session = db_session

    def process(self):
        """"""
        self.start_time = datetime.now()
        try:
            self.process_data()
        except Exception:
            self.status_code = constants.FAILURE_CODE_LABEL
            err_msg = traceback.format_exc()
            LOGGER.critical('Error detail is following:%s' % err_msg)
        finally:
            self.clean_up()

    def process_data(self):
        """"""
        self.fetch_data()
        index = 1
        while len(self.records):
            LOGGER.info('| Processing (%d of %d) school record',
                        index, self.total_fetched_records)
            index += 1
            row = self.records.pop()
            try:
                self.serialize_data(row)
                self.save()
            except Exception:
                self.db_session.rollback()
                self.status_code = constants.FAILURE_CODE_LABEL
                msg = ('Exception occurred while processing record.\nGiven '
                       'raw data:\n%s\nException traceback:\n%s'
                       % (row, traceback.format_exc()))
                LOGGER.critical(msg)

    def fetch_data(self):
        """"""
        LOGGER.info('------------------------------------')
        LOGGER.info('|        Fetch Appointment(s)       |')
        LOGGER.info('------------------------------------')
        LOGGER.debug('Clearing appointments list')
        file_names = []
        for file_name in os.listdir(settings.FILES_PATH):
            if not fnmatch(file_name, constants.COMPLETED_FILE_NAME_PATTERN):
                file_names.append(file_name)

        file_names = filter(self.filter_files, file_names)
        if file_names:
            file_names.sort()
            file_path = file_names[0]
            file_path = os.path.join(settings.FILES_PATH, file_path)
            self.file_path = os.path.normpath(file_path)
            excel_common = excel_helper.ExcelCommon(file_path=self.file_path)
            self.records.extendleft(excel_common.get_records())
            self.total_fetched_records = excel_common.total_records
        LOGGER.info('| Schools Records loaded: %d' % self.total_fetched_records)
        LOGGER.info('------------------------------')

    def filter_files(self, _file):
        """"""
        if '.keep' in _file:
            return False

        return True

    def serialize_data(self, row):
        """"""
        self.data_container = DataContainer()
        self.data_container.school_obj = self.serialize_school_data(row)
        self.data_container.enrollment_obj = self.serialize_enrollment_data(row)
        self.data_container.teaching_staff_obj = self.serialize_teaching_staff_data(row)
        self.data_container.academic_facilities_obj = self.serialize_academic_facilities_data(row)
        self.data_container.basic_facilities_obj = self.serialize_basic_facilities_data(row)
        self.data_container.sports_facilities_obj = self.serialize_sports_facilities_data(row)

    def serialize_school_data(self, row):
        """

        :param row:
        :return:
        """
        school_obj = school.School()
        for field in constants.SCHOOL_FIELDS:
            value  = row[field]
            if (type(school_obj.__table__.c[field].type) == sql.sqltypes.Integer
                    and value in settings.NULLS):
                value = 0
            elif (type(school_obj.__table__.c[field].type) == sql.sqltypes.Integer
                    and value not in settings.NULLS):
                value = int(value)
            if (isinstance(school_obj.__table__.c[field].type, DateTime)
                    and value not in settings.NULLS):
                try:
                    datetime_value = xlrd.xldate_as_tuple(row[field],
                                                          xlrd.Book.datemode)
                    value = datetime(datetime_value[0], datetime_value[1],
                                     datetime_value[2], datetime_value[3],
                                     datetime_value[4], datetime_value[5])
                except Exception:
                    err_msg = traceback.format_exc()
                    LOGGER.debug('Error detail:%s', err_msg)
                    value = ''
            setattr(school_obj, field, value)
        return school_obj

    def serialize_enrollment_data(self, row):
        """

        :param row:
        :return:
        """
        enrollment_obj = school.Enrollment()
        for field in constants.ENROLLMENT_FIELDS:
            value = row[field]
            if (type(enrollment_obj.__table__.c[field].type) ==
                    sql.sqltypes.Integer and value in settings.NULLS):
                value = 0
            setattr(enrollment_obj, field, value)
        return enrollment_obj

    def serialize_teaching_staff_data(self, row):
        """

        :param row:
        :return:
        """
        teaching_staff_obj = school.TeachingStaff()
        for field in constants.TEACHING_STAFF_FIELDS:
            value = row[field]
            if (type(teaching_staff_obj.__table__.c[field].type) ==
                    sql.sqltypes.Integer and value in settings.NULLS):
                value = 0
            setattr(teaching_staff_obj, field, value)
        if teaching_staff_obj.sanctioned not in settings.NULLS and (
                    teaching_staff_obj.filled not in settings.NULLS):
            teaching_staff_obj.vacant = int(teaching_staff_obj.sanctioned) - (
                int(teaching_staff_obj.filled))
        return teaching_staff_obj

    def serialize_academic_facilities_data(self, row):
        """

        :param row:
        :return:
        """
        academic_facilities_obj = facilities.AcademicFacilities()
        for field in constants.ACADEMIC_FACILITIES_FIELDS:
            value = row[field]
            if (type(academic_facilities_obj.__table__.c[field].type) ==
                    sql.sqltypes.Integer and value in settings.NULLS):
                value = 0
            setattr(academic_facilities_obj, field, value)
        return academic_facilities_obj

    def serialize_basic_facilities_data(self, row):
        """

        :param row:
        :return:
        """
        basic_facilities_obj = facilities.BasicFacilities()
        for field in constants.BASIC_FACILITIES_FIELDS:
            value = row[field]
            if (type(basic_facilities_obj.__table__.c[field].type) ==
                    sql.sqltypes.Integer and value in settings.NULLS):
                value = 0
            setattr(basic_facilities_obj, field, value)
        return basic_facilities_obj

    def serialize_sports_facilities_data(self, row):
        """

        :param row:
        :return:
        """
        sports_facilities_obj = facilities.SportsFacilities()
        for field in constants.SPORTS_FACILITIES_FIELDS:
            value = row[field]
            if (type(sports_facilities_obj.__table__.c[field].type) ==
                    sql.sqltypes.Integer and value in settings.NULLS):
                value = 0
            setattr(sports_facilities_obj, field, value)
        return sports_facilities_obj

    def save(self):
        """"""
        try:
            self.save_school()
            self.save_enrollment()
            self.save_teaching_staff()
            self.save_academic_facilities()
            self.save_basic_facilities()
            self.save_sports_facilities()
        except Exception:
            self.db_session.rollback()
            self.status_code = constants.FAILURE_CODE_LABEL
            msg = ('Exception occurred while processing record.\nGiven '
                   'school id:\n%s\nException traceback:\n%s'
                   % (self.data_container.school_obj.emiscode,
                      traceback.format_exc()))
            LOGGER.critical(msg)
        else:
            self.db_session.commit()
            self.total_saved_records += 1

    def save_school(self):
        """"""
        school_obj = school.School.get_by_id(self.data_container.school_obj.emiscode)
        if not school_obj:
            school.School.save(self.data_container.school_obj)
        else:
            kwargs = {}
            for field in constants.SCHOOL_FIELDS:
                kwargs[field] = getattr(self.data_container.school_obj, field)
                kwargs['record_update_date'] = datetime.utcnow()
            school_obj.update(**kwargs)

    def save_enrollment(self):
        """"""
        enrollment_obj = school.Enrollment.get_by_id(
            self.data_container.enrollment_obj.emiscode)
        if not enrollment_obj:
            school.Enrollment.save(self.data_container.enrollment_obj)
        else:
            kwargs = {}
            for field in constants.ENROLLMENT_FIELDS:
                kwargs[field] = getattr(self.data_container.enrollment_obj, field)
            enrollment_obj.update(**kwargs)

    def save_teaching_staff(self):
        """"""
        teaching_staff_obj = school.TeachingStaff.get_by_id(
            self.data_container.teaching_staff_obj.emiscode)
        if not teaching_staff_obj:
            school.TeachingStaff.save(self.data_container.teaching_staff_obj)
        else:
            kwargs = {}
            for field in constants.TEACHING_STAFF_FIELDS:
                kwargs[field] = getattr(self.data_container.teaching_staff_obj,
                                        field)
            teaching_staff_obj.update(**kwargs)

    def save_academic_facilities(self):
        """"""
        academic_facilities_obj = facilities.AcademicFacilities.get_by_id(
            self.data_container.academic_facilities_obj.emiscode)
        if not academic_facilities_obj:
            facilities.AcademicFacilities.save(
                self.data_container.academic_facilities_obj)
        else:
            kwargs = {}
            for field in constants.ACADEMIC_FACILITIES_FIELDS:
                kwargs[field] = getattr(
                    self.data_container.academic_facilities_obj, field)
            academic_facilities_obj.update(**kwargs)

    def save_basic_facilities(self):
        """"""
        basic_facilities_obj = facilities.BasicFacilities.get_by_id(
            self.data_container.academic_facilities_obj.emiscode)
        if not basic_facilities_obj:
            facilities.BasicFacilities.save(
                self.data_container.basic_facilities_obj)
        else:
            kwargs = {}
            for field in constants.BASIC_FACILITIES_FIELDS:
                kwargs[field] = getattr(
                    self.data_container.basic_facilities_obj, field)
            basic_facilities_obj.update(**kwargs)

    def save_sports_facilities(self):
        """"""
        sports_facilities_obj = facilities.SportsFacilities.get_by_id(
            self.data_container.sports_facilities_obj.emiscode)
        if not sports_facilities_obj:
            facilities.SportsFacilities.save(
                self.data_container.sports_facilities_obj)
        else:
            kwargs = {}
            for field in constants.SPORTS_FACILITIES_FIELDS:
                kwargs[field] = getattr(
                    self.data_container.sports_facilities_obj, field)
                sports_facilities_obj.update(**kwargs)

    def log_summary(self):
        """"""
        end_time = datetime.now()
        LOGGER.debug('Cleanser processing completed at: %s', end_time)
        LOGGER.info('------------------------------------')
        LOGGER.info('| Total fetched records: %s' % self.total_fetched_records)
        LOGGER.info('| Total saved records: %s' % self.total_saved_records)
        LOGGER.info("| Time taken: %s" % (end_time - self.start_time))
        LOGGER.info('------------------------------------')

    def rename_or_delete_processed_file(self):
        """"""
        if self.delete_file:
            excel_helper.ExcelCommon.delete_csv(self.file_path)
        else:
            excel_helper.ExcelCommon.rename_file(self.file_path)

    def clean_up(self):
        """"""
        self.log_summary()
        if self.file_path and self.status_code == constants.SUCCESS_CODE_LABEL:
            self.rename_or_delete_processed_file()


class DataContainer:

    def __init__(self):
        self.school_obj = None
        self.enrollment_obj = None
        self.teaching_staff_obj = None
        self.academic_facilities_obj = None
        self.basic_facilities_obj = None
        self.sports_facilities_obj = None
