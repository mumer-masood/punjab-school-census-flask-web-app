"""

"""
import xlrd
import logging
import os
from datetime import datetime

import constants
import settings

LOGGER = logging.getLogger(__file__)

NULLS = settings.NULLS[:]


class ExcelCommon(object):
    def __init__(self, **kwargs):
        self.file_path = kwargs['file_path']
        self.headers = None
        self.total_records = 0

    def get_file_path(self):
        if self.file_path:
            return os.path.normpath(self.file_path)
        return ''

    def get_records(self):
        """"""

        all_rows = []
        rows = self.get_data_rows()
        for row in rows:
            all_rows.append(dict(zip(self.headers, row)))
        self.total_records = len(all_rows)
        return all_rows

    def get_data_rows(self):
        """
        Get data from Excel file, set header row and also clean bad rows
        :return: List of valid records
        """
        try:
            _book = xlrd.open_workbook(self.file_path)
        except IOError:
            LOGGER.warning('Unable to open file: %s' % self.file_path)
            raise
        else:
            sheet = _book.sheet_by_index(0)
            rows = map(self.get_row_data, sheet.get_rows())
            self.set_header(rows)
            filtered_rows = filter(self.validate_row, rows)

        return filtered_rows

    def get_row_data(self, row):
        """"""
        row_data = [cell.value for cell in row]
        row_data = ['' if (isinstance(item, basestring) and
                           item.strip().lower() in NULLS)
                    else item for item in row_data]

        return row_data

    def validate_row(self, row):
        """"""
        if self.is_empty_row(row):
            LOGGER.debug('bad empty row= %s ' % str(row))
            return False
        if constants.EMISCODE_KEY in row:
            LOGGER.debug('it is header row')
            return False
        if len(row) != len(self.headers):
            LOGGER.debug('Row size:%d is bad= %s ' % (len(row), str(row)))
            return False

        return True

    def is_empty_row(self, row):
        """"""
        is_row_valid = True
        for value in row:
            if ((isinstance(value, basestring) and value.strip() not in NULLS)
                    or value not in NULLS):
                is_row_valid = False
                break

        return is_row_valid

    def set_header(self, rows):
        """"""
        for row in rows:
            if not self.is_empty_row(row) and constants.EMISCODE_KEY in row:
                self.headers = row
                self.headers = [col_header.lower() for col_header in
                                self.headers]
                LOGGER.debug('Headers are= %s ' % self.headers)
                break
        if self.headers is None:
            LOGGER.critical(msg=('Unable to find Header in file:%s' %
                                 self.file_path))


    @classmethod
    def rename_file(cls, file_path, append_str="completed"):
        """Given file path, renames file by appending <append_str><datetime>
           . Returns renamed file name"""
        file_path = os.path.normpath(file_path)
        csv_dir = os.path.dirname(file_path)
        csv_file = os.path.basename(file_path)
        file, ext = os.path.splitext(csv_file)
        csv_file = '%s_%s_%s%s' % (append_str, datetime.now().strftime(
            "%Y%m%d%H%M%S"), file, ext)
        renamed_path = os.path.join(csv_dir, csv_file)
        LOGGER.info('Excel File path: %s' % (file_path))
        os.rename(file_path, renamed_path)
        return csv_file

    @classmethod
    def delete_csv(cls, file_path):
        file_path = os.path.normpath(file_path)
        os.remove(file_path)

