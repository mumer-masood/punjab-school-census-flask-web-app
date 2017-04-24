"""Model School unit tests. This file contains test for methods in School
model."""
import math

import pytest

from schoolCensus import constants
from schoolCensus.school_models import models


@pytest.mark.usefixtures('session')
class TestSchoolModelMethodGetDistricts:
    """Contains unit tests for get_districts(), which is School model."""

    def test_get_school_by_id(self):
        """Get school by by primary key i.e emiscode."""
        school = models.School(emiscode=12)
        school.save()

        retrieved = models.School.get_by_id(school.emiscode)
        assert retrieved == school
        assert retrieved.emiscode == school.emiscode
        assert retrieved.dist_id == school.dist_id

    def test_get_districts_with_no_record_in_db(self):
        """In this test no districts exist in database so get_districts method
        should return a empty list."""

        retrieved = models.School.get_districts()
        assert retrieved == []

    def test_get_districts_with_one_record_in_db(self):
        """In this test one district exist in database so get_districts method
        returns list containing one record."""

        first_school = models.School(dist_id=123, dist_nm='TestCity')
        first_school.save()
        retrieved = models.School.get_districts()
        assert len(retrieved) == 1
        assert retrieved[0].dist_id == first_school.dist_id
        assert retrieved[0].dist_nm == first_school.dist_nm

    def test_get_districts_with_with_dist_id(self):
        """In this test one district exist in database and get_districts method
        is called with this record district id."""

        first_school = models.School(dist_id=123, dist_nm='TestCity')
        first_school.save()
        retrieved = models.School.get_districts(first_school.dist_id)
        assert retrieved.dist_id == first_school.dist_id
        assert retrieved.dist_nm == first_school.dist_nm


class TestSchoolModelMethodDistrictEachSchoolStudentsTeacherRatio:
    """School model method district_each_school_students_teacher_ratio tests.
    In this test case we add record for school, Enrollment and TeachingStaff
    in database and call method district_each_school_students_teacher_ratio().
    We test that ratio returned by this method is according to test data."""
    @pytest.mark.parametrize('description, test_input, expected', [
        ('In this test no districts data exist in database so method should '
         'return a empty list.',
         [], []),
        ('In this test one district record exist in database so method should '
         'return a list of length one and ratio value 0 as total number of '
         'students and total number of teachers(filled) value is 0.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=0, filled=0)],
         [[1, 0]]),
        ('In this test one districts record exist in database so method should '
         'return a list of length one and ration value 0 as total number of '
         'teachers(filled) value is 5 but total number of students value 0.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=0, filled=5)],
         [[1, 0]]),
        ('In this test one districts record exist in database so method should '
         'return a list of length one and ratio value 0 as total number of '
         'students value is 5 but total number of teachers(filled) value is 0.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=5, filled=0)],
         [[1, 0]]),
        ('In this test one districts record exist in database so method should '
         'return a list of length one and ratio value 1 as total number of '
         'students value is 5 and total number of teachers(filled) value is 5.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=5, filled=5)],
         [[1, 1]]),
        ('In this test one districts record exist in database so method should '
         'return a list of length one and ratio value 1 as total number of '
         'student value is 5 and total number of teachers(filled) value is 10.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=5, filled=10)],
         [[1, 1]]),
        ('In this test two records for district id 1 exist in database so '
         'method should return a list of length two and ratio value 7 and 6.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=40, filled=6),
          dict(emiscode=13, dist_id=1, total_no_of_students=23, filled=4)],
         [[1, 7], [2, 6]]),
        ('In this test two records exist in database but only one record for '
         'district id 1 so method should return a list of length one and ratio '
         'value 6.',
         [dict(emiscode=12, dist_id=1, total_no_of_students=50, filled=9),
          dict(emiscode=13, dist_id=2, total_no_of_students=48, filled=7)],
         [[1, 6]])
    ])
    def test_get_districts_with_with_dist_id(self, session, description,
                                             test_input, expected):
        """In this test we add school, enrollment and teaching staff record in
        database according to test input and test method
        district_each_school_students_teacher_ratio give expected output."""

        for test_data in test_input:
            school = models.School(emiscode=test_data['emiscode'],
                                   dist_id=test_data['dist_id'])
            session.add(school)
            enrollment = models.Enrollment(
                emiscode=test_data['emiscode'],
                total_no_of_students=test_data['total_no_of_students'])
            session.add(enrollment)
            teaching_staff = models.TeachingStaff(
                emiscode=test_data['emiscode'], filled=test_data['filled'])
            session.add(teaching_staff)
        session.commit()

        retrieved = models.School.district_each_school_students_teacher_ratio(1)
        assert len(retrieved) == len(expected)
        assert retrieved == expected


def test_get_school_total_teachers(session):
    """In this test, we test that total number of teachers in district returned
    by district_schools_total_teachers() method is equal to test data."""
    school = models.School(emiscode=12, dist_id=1)
    session.add(school)
    teaching_staff = models.TeachingStaff(emiscode=12, filled=5)
    session.add(teaching_staff)
    session.commit()

    retrieved = models.School.district_schools_total_teachers(school.dist_id)
    assert retrieved == teaching_staff.filled


def test_get_school_total_student(session):
    """In this test, we test that total number of student in district returned
    by district_schools_total_students() method is equal to test data."""
    school = models.School(emiscode=12, dist_id=1)
    session.add(school)
    enrollment = models.Enrollment(emiscode=12, total_no_of_students=5)
    session.add(enrollment)
    session.commit()

    retrieved = models.School.district_schools_total_students(school.dist_id)
    assert retrieved == enrollment.total_no_of_students


def test_get_student_teacher_ratio(session):
    """In this test, we test that student and teacher ratio in district returned
    by district_schools_students_teacher_ratio() method is equal to test
    data."""
    school = models.School(emiscode=12, dist_id=1)
    session.add(school)
    enrollment = models.Enrollment(emiscode=12, total_no_of_students=5)
    session.add(enrollment)
    teaching_staff = models.TeachingStaff(emiscode=12, filled=5)
    session.add(teaching_staff)
    session.commit()

    retrieved = models.School.district_schools_students_teacher_ratio(
        school.dist_id)
    assert retrieved == math.ceil(
        enrollment.total_no_of_students/teaching_staff.filled)


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and count all is false so method '
     'should return 0.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=False,
          school_data=[]), 0),
    ('In this test no data exist in database and count all is true so method '
     'should return 0.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=True,
          school_data=[]), 0),
    ('In this test one record exist in database and count all is false so '
     'method should return 0 as record does not fulfill the criteria.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), count_all=False, dist_id=None,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 0),
    ('In this test one record exist in database and record does not fulfill the'
     'criteria but method should return 1 as count all is true.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 1),
    ('In this test we test the equal operator. One record exist in database '
     'and count all is true but method should return 0 as dist_id is different '
     'then the record dist_id.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=2, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 0),
    ('In this test we test the equal operator. One record exist in database. '
     'The dist_id is same as the record dist_id but record does not fulfills '
     'the criteria but method should return 1 as count all is true ',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=1, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 1),
    ('In this test we test the equal operator. One record exist in database. '
     'The method should return 0 as record does not fulfill the criteria.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 0),
    ('In this test we test the equal operator. One record exist in database. '
     'The method should return 0 as record fulfill the criteria but district '
     'id of record is different then dist_id.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=2, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0)]), 0),
    ('In this test we test the equal operator. One record exist in database. '
     'The dist_id is same as record dist_id but method should return 0 as '
     'record does not fulfill the criteria.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)]), 0),
    ('In this test we test the equal operator. One record exist in database. '
     'The dist_id is same as record dist_id and method should return 1 as '
     'record fulfills the criteria.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0)]), 1),
    ('In this test we test the equal operator. One record exist in database. '
     'The dist_id is not given but method should return 1 as record fulfills '
     'the criteria.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0)]), 1),
    ('In this test we test the equal operator. Two record exist in database. '
     'Both record fulfills the criteria but the dist_id of one record is '
     'different then given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)]), 1),
    ('In this test we test the equal operator. Two record exist in database. '
     'Both record fulfills the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.EQUAL_OP, field_name='medium',
                        value=0), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)]), 2),
    ('In this test we test the less than operator. 2 record exist in database. '
     'Both record does not fulfill the criteria so method should return 0.',
     dict(criteria=dict(operator=constants.LESS_THAN_OP, field_name='medium',
                        value=0), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)]), 0),
    ('In this test we test the less than operator. 2 record exist in database. '
     'Both record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.LESS_THAN_OP, field_name='medium',
                        value=1), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)]), 2),
    ('In this test we test the less than operator. 2 record exist in database. '
     'Both record fulfill the criteria but dist_id of one record is different '
     'than given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.LESS_THAN_OP, field_name='medium',
                        value=1), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)]), 1),
    ('In this test we test less than equal to operator. Two record exist in '
     'database. Both record does not fulfill the criteria so method should '
     'return 0.',
     dict(criteria=dict(operator=constants.LESS_THAN_EQUAL_TO_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=2),
                       dict(emiscode=13, dist_id=1, medium=2)]), 0),
    ('In this test we test less than equal to operator. Two record exist in '
     'database. Both record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.LESS_THAN_EQUAL_TO_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=1)]), 2),
    ('In this test we test less than equal to operator. Two record exist in '
     'database. Both record fulfill the criteria but dist_id of one record is '
     'different than given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.LESS_THAN_EQUAL_TO_OP, value=1,
                        field_name='medium'), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)]), 1),
    ('In this test we test greater than operator. 2 record exist in database. '
     'Both record does not fulfill the criteria so method should return 0.',
     dict(criteria=dict(operator=constants.GREATER_THAN_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)]), 0),
    ('In this test we test greater than operator. 2 record exist in database. '
     'Both record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.GREATER_THAN_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=2),
                       dict(emiscode=13, dist_id=1, medium=2)]), 2),
    ('In this test we test greater than operator. 2 record exist in database. '
     'Both record fulfill the criteria but dist_id of one record is different '
     'than given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.GREATER_THAN_OP, value=0,
                        field_name='medium'), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=2, medium=1)]), 1),
    ('In this test we test greater than equal to operator. Two record exist in '
     'database. Both record does not fulfill the criteria so method should '
     'return 0.',
     dict(criteria=dict(operator=constants.GREATER_THAN_EQUAL_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)]), 0),
    ('In this test we test greater than equal to operator. Two record exist in '
     'database. Both record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.GREATER_THAN_EQUAL_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=2),
                       dict(emiscode=13, dist_id=1, medium=1)]), 2),
    ('In this test we test greater than equal to operator. Two record exist in '
     'database. Both record fulfill the criteria but dist_id of one record is '
     'different than given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.GREATER_THAN_EQUAL_OP, value=0,
                        field_name='medium'), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=2, medium=1)]), 1),
    ('In this test we test in operator. Two record exist in database. Both '
     'record does not fulfill the criteria so method should return 0.',
     dict(criteria=dict(operator=constants.IN_OP, value=[0, 1],
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=3),
                       dict(emiscode=13, dist_id=1, medium=4)]), 0),
    ('In this test we test in operator. Two record exist in database. Both '
     'record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.IN_OP, value=(0, 2),
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=2)]), 2),
    ('In this test we test in operator. Two record exist in database. Only one '
     'record fulfill the criteria so method should return 1.',
     dict(criteria=dict(operator=constants.IN_OP, value=(1, 2),
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=2)]), 1),
    ('In this test we test in operator. Two record exist in database. Both '
     'record fulfill the criteria but dist_id of one record is different than '
     'given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.IN_OP, value=[0, 2],
                        field_name='medium'), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=2)]), 1),
    ('In this test we test not operator. Two record exist in database. Both '
     'record does not fulfill the criteria so method should return 0.',
     dict(criteria=dict(operator=constants.NOT_OP, value=1,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=1, medium=1)]), 0),
    ('In this test we test not operator. Two record exist in database. Both '
     'record fulfill the criteria so method should return 2.',
     dict(criteria=dict(operator=constants.NOT_OP, value=2,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=1, medium=1)]), 2),
    ('In this test we test not operator. Two record exist in database. Only '
     'one record fulfill the criteria so method should return 1.',
     dict(criteria=dict(operator=constants.NOT_OP, value=2,
                        field_name='medium'), dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=2),
                       dict(emiscode=13, dist_id=1, medium=1)]), 1),
    ('In this test we test not operator. Two record exist in database. Both '
     'record fulfill the criteria bt dist_id of one record is different than '
     'given dist_id so method should return 1.',
     dict(criteria=dict(operator=constants.NOT_OP, value=0,
                        field_name='medium'), dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=2, medium=1)]), 1)])
def test_get_same_table_count(description, test_input, expected, session):
    """In this test, we add record in School table depending on test data
    and verify that count returned by get_same_table_count() method is according
    to test data."""
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_same_table_count(
        test_input['criteria'], test_input['dist_id'], test_input['count_all'])
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and count all is false so method '
     'should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[],
          sports_facility_data=[]), 0),
    ('In this test no data exist in database and count all is true so method '
     'should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=True,
          school_data=[],
          sports_facility_data=[]), 0),
    ('In this test School record exist but SportsFacilities record does not '
     'exist in database and count all is False so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[]), 0),
    ('In this test School record exist but SportsFacilities record does not '
     'exist in database and count all is True so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[]), 0),
    ('In this test School and SportsFacilities record exist in database but it '
     'does not fulfill criteria but method should return 1 as count all is '
     'True.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=1)]), 1),
    ('In this test School and SportsFacilities record exist in database but it '
     'does not fulfill criteria and dist_id of record is same as given dist_id '
     'so method should return 1 as count all is True.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=1,
          count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=1)]), 1),
    ('In this test School and SportsFacilities record exist in database but it '
     'does not fulfill criteria, count all is True and dist_id of record is '
     'not same as given dist_id so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=2,
          count_all=True,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=1)]), 0),
    ('In this test School and SportsFacilities record exist in database but it '
     'does not fulfill criteria so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=1)]), 0),
    ('In this test School and SportsFacilities record exist in database. It '
     'fulfills criteria so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0)]), 1),
    ('In this test School and SportsFacilities record exist in database. It '
     'fulfills criteria but given dist_id is different than record dist_id so '
     'method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=2,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0)]), 0),
    ('In this test two School and SportsFacilities record exist in database. '
     'Both records fulfills criteria so method should return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=2, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 2),
    ('In this test two School and SportsFacilities record exist in database. '
     'Both records fulfill criteria but for one record dist_id is different '
     'than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=1,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=2, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 1),
    ('In this test two School and SportsFacilities record exist in database. '
     'Only one record fulfills criteria so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=1,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=1)]), 1),
    ('In this test two School and SportsFacilities record exist in database. '
     'Both records fulfill criteria so method should return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.EQUAL_OP, value=0), dist_id=1,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=1),
                       dict(emiscode=13, dist_id=1, medium=1)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 2),
    ('In this test we test less than operator. Two School and SportsFacilities '
     'record exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_OP, value=0), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 0),
    ('In this test we test less than operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_OP, value=1), dist_id=None,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 2),
    ('In this test we test less than operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria but dist_id for '
     'one record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_OP, value=1), dist_id=1,
          count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=0)]), 1),
    ('In this test we test less than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_EQUAL_TO_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=2)]), 0),
    ('In this test we test less than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_EQUAL_TO_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=1)]), 2),
    ('In this test we test less than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'but dist_id for one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.LESS_THAN_EQUAL_TO_OP, value=1),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=1)]), 1),
    ('In this test we test greater than operator. Two School and '
     'SportsFacilities record exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=1)]), 0),
    ('In this test we test greater than operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=3)]), 2),
    ('In this test we test greater than operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'but dist_id for one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_OP, value=1),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=4)]), 1),
    ('In this test we test greater than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_EQUAL_OP, value=2),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=1)]), 0),
    ('In this test we test greater than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_EQUAL_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=1),
                                dict(emiscode=13, hockey=2)]), 2),
    ('In this test we test greater than equal to operator. Two School and '
     'SportsFacilities record exist in database. Both records fulfill criteria '
     'but dist_id for one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.GREATER_THAN_EQUAL_OP, value=1),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=3)]), 1),
    ('In this test we test in operator. Two School and SportsFacilities record '
     'exist in database. Both records does not fulfill criteria so method '
     'should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.IN_OP, value=[0, 1]),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=3)]), 0),
    ('In this test we test in operator. Two School and SportsFacilities record '
     'exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.IN_OP, value=(0, 2)),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=2)]), 2),
    ('In this test we test in operator. Two School and SportsFacilities record '
     'exist in database. Only one records fulfill criteria so method should '
     'return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.IN_OP, value=(1, 2)),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=2)]), 1),
    ('In this test we test in operator. Two School and SportsFacilities record '
     'exist in database. Both records fulfill criteria but dist_id for one '
     'record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.IN_OP, value=[0, 2]),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=0),
                                dict(emiscode=13, hockey=2)]), 1),
    ('In this test we test not operator. Two School and SportsFacilities '
     'record exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.NOT_OP, value=1),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=1),
                                dict(emiscode=13, hockey=1)]), 0),
    ('In this test we test not operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.NOT_OP, value=2),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=1),
                                dict(emiscode=13, hockey=1)]), 2),
    ('In this test we test not operator. Two School and SportsFacilities '
     'record exist in database. Only one records fulfill criteria so method '
     'should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.NOT_OP, value=2),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=1, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=2),
                                dict(emiscode=13, hockey=1)]), 1),
    ('In this test we test not operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria but dist_id for '
     'one record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='SportsFacilities', field_name='hockey',
                        operator=constants.NOT_OP, value=0),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1, medium=0),
                       dict(emiscode=13, dist_id=2, medium=0)],
          sports_facility_data=[dict(emiscode=12, hockey=1),
                                dict(emiscode=13, hockey=1)]), 1),
    ('In this test we test and operator. Two School and SportsFacilities '
     'record exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(
         criteria=dict(operator=constants.AND_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=1, football=2),
                               dict(emiscode=13, hockey=2, football=1)]), 0),
    ('In this test we test and operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(
         criteria=dict(operator=constants.AND_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=2, football=2),
                               dict(emiscode=13, hockey=2, football=3)]), 2),
    ('In this test we test and operator. Two School and SportsFacilities '
     'record exist in database. Only one records fulfill criteria so method '
     'should return 1.',
     dict(
         criteria=dict(operator=constants.AND_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=2, football=2),
                               dict(emiscode=13, hockey=1, football=1)]), 1),
    ('In this test we test and operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria but dist_id for '
     'one record is different than given dist_id so method should return 1.',
     dict(
         criteria=dict(operator=constants.AND_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=1, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=2, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=2, football=2),
                               dict(emiscode=13, hockey=2, football=3)]), 1),
    ('In this test we test or operator. Two School and SportsFacilities '
     'record exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(
         criteria=dict(operator=constants.OR_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=1, football=1),
                               dict(emiscode=13, hockey=1, football=1)]), 0),
    ('In this test we test or operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(
         criteria=dict(operator=constants.OR_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=1, football=2),
                               dict(emiscode=13, hockey=2, football=1)]), 2),
    ('In this test we test or operator. Two School and SportsFacilities '
     'record exist in database. Only one records fulfill criteria so method '
     'should return 1.',
     dict(
         criteria=dict(operator=constants.OR_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=None, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=1, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=1, football=1),
                               dict(emiscode=13, hockey=2, football=2)]), 1),
    ('In this test we test or operator. Two School and SportsFacilities '
     'record exist in database. Both records fulfill criteria but dist_id for '
     'one record is different than given dist_id so method should return 1.',
     dict(
         criteria=dict(operator=constants.OR_OP, field_model='SportsFacilities',
                       operator_fields=[dict(
                           field_name='hockey', query_class='SportsFacilities',
                           operator=constants.EQUAL_OP, value=2),
                           dict(field_name='football', operator=constants.NOT_OP,
                                query_class='SportsFacilities',  value=1)]),
         dist_id=1, count_all=False,
         school_data=[dict(emiscode=12, dist_id=1, medium=0),
                      dict(emiscode=13, dist_id=2, medium=0)],
         sports_facility_data=[dict(emiscode=12, hockey=2, football=2),
                               dict(emiscode=13, hockey=2, football=2)]), 1)])
def test_get_join_table_count(description, test_input, expected, session):
    """In this test, we add record in School and SportFacilities table according
    to test data and verify that count returned by get_join_table_count() method
    is according to test data."""
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facility_data']:
        sports_facility = models.SportsFacilities(**test_data)
        session.add(sports_facility)
    session.commit()
    retrieved = models.School.get_join_table_count(
        test_input['criteria'], test_input['dist_id'], test_input['count_all'])
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and count all is false so method '
     'should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[],
          basic_facility_data=[]), 0),
    ('In this test no data exist in database and count all is true so method '
     'should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=True,
          school_data=[],
          basic_facility_data=[]), 0),
    ('In this test School record exist but BasicFacilities record does not '
     'exist in database and count all is False so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[]), 0),
    ('In this test School record exist but BasicFacilities record does not '
     'exist in database and count all is True so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[]), 0),
    ('In this test School and BasicFacilities record exist in database but it '
     'does not fulfill criteria but method should return 1 as count all is '
     'True.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=1)]), 1),
    ('In this test School and BasicFacilities record exist in database but it '
     'does not fulfill criteria and dist_id of record is same as given dist_id '
     'so method should return 1 as count all is True.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=1)]), 1),
    ('In this test School and BasicFacilities record exist in database. It '
     'fulfills criteria, dist_id of record is different than given dist_id '
     'so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=2, count_all=True,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=1)]), 0),
    ('In this test School and BasicFacilities record exist in database. It '
     'does not fulfill criteria so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=2)]), 0),
    ('In this test School and BasicFacilities record exist in database. It '
     'fulfills criteria so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4)]), 1),
    ('In this test School and BasicFacilities record exist in database. It '
     'fulfills criteria but recoord dist_id is different than given dist_id so '
     'method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=2, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=1, toilets_total=2)]), 0),
    ('In this test two School and BasicFacilities record exist in database. '
     'Both records fulfills criteria so method should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=6)]), 2),
    ('In this test two School and BasicFacilities record exist in database. '
     'Both records fulfills criteria but dist_id of one record is different '
     'than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=6)]), 1),
    ('In this test two School and BasicFacilities record exist in database. '
     'Only one record fulfills criteria so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=4, toilets_total=6)]), 1),
    ('In this test two School and BasicFacilities record exist in database. '
     'Both records fulfills criteria so method should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.EQUAL_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=6)]), 2),
    ('In this test we test less than operator. Two School and BasicFacilities '
     'records exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=4, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=4)]), 0),
    ('In this test we test less than operator. Two School and BasicFacilities '
     'records exist in database. Both records fulfill criteria so method '
     'should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=1, toilets_total=4),
              dict(emiscode=13, toilet_usable=1, toilets_total=3)]), 2),
    ('In this test we test less than operator. Two School and BasicFacilities '
     'records exist in database. Both records fulfill criteria but dist_id of '
     'one record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=1, toilets_total=4),
              dict(emiscode=13, toilet_usable=2, toilets_total=6)]), 1),
    ('In this test we test less than equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_EQUAL_TO_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=4, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=4)]), 0),
    ('In this test we test less than equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_EQUAL_TO_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=6),
              dict(emiscode=13, toilet_usable=1, toilets_total=4)]), 2),
    ('In this test we test less equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'but dist_id of one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.LESS_THAN_EQUAL_TO_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=6),
              dict(emiscode=13, toilet_usable=2, toilets_total=8)]), 1),
    ('In this test we test greater than operator. Two School and '
     'BasicFacilities records exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=1, toilets_total=4),
              dict(emiscode=13, toilet_usable=2, toilets_total=6)]), 0),
    ('In this test we test greater than operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=4),
              dict(emiscode=13, toilet_usable=5, toilets_total=6)]), 2),
    ('In this test we test greater than operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'but dist_id of one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=4, toilets_total=5),
              dict(emiscode=13, toilet_usable=5, toilets_total=6)]), 1),
    ('In this test we test greater than equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records does not fulfill '
     'criteria so method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_EQUAL_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=1),
              dict(emiscode=13, toilet_usable=3, toilets_total=7)]), 0),
    ('In this test we test greater than equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'so method should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_EQUAL_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=4)]), 2),
    ('In this test we test greater than equal to operator. Two School and '
     'BasicFacilities records exist in database. Both records fulfill criteria '
     'but dist_id of one record is different than given dist_id so method '
     'should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.GREATER_THAN_EQUAL_OP,
                        field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=4),
              dict(emiscode=13, toilet_usable=5, toilets_total=6)]), 1),
    ('In this test we test in operator. Two School and BasicFacilities records '
     'exist in database. Both records does not fulfill criteria so method '
     'should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=[50, 75],
                        operator=constants.IN_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=0, toilets_total=1),
              dict(emiscode=13, toilet_usable=4, toilets_total=5)]), 0),
    ('In this test we test in operator. Two School and BasicFacilities records '
     'exist in database. Both records fulfill criteria so method should '
     'return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=(50, 75),
                        operator=constants.IN_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=4)]), 2),
    ('In this test we test in operator. Two School and BasicFacilities records '
     'exist in database. Only one records fulfill criteria so method should '
     'return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=(50, 75),
                        operator=constants.IN_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=6),
              dict(emiscode=13, toilet_usable=1, toilets_total=4)]), 1),
    ('In this test we test in operator. Two School and BasicFacilities records '
     'exist in database. Both records fulfill criteria but dist_id of one '
     'record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=[50, 75],
                        operator=constants.IN_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=4),
              dict(emiscode=13, toilet_usable=2, toilets_total=4)]), 1),
    ('In this test we test not operator. Two School and BasicFacilities '
     'records exist in database. Both records does not fulfill criteria so '
     'method should return 0.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.NOT_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=3, toilets_total=6)]), 0),
    ('In this test we test not operator. Two School and BasicFacilities '
     'records exist in database. Both records fulfill criteria so method '
     'should return 2.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.NOT_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=3, toilets_total=4),
              dict(emiscode=13, toilet_usable=2, toilets_total=6)]), 2),
    ('In this test we test not operator. Two School and BasicFacilities '
     'records exist in database. Only one records fulfill criteria so method '
     'should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.NOT_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=None, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=1)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=2, toilets_total=4),
              dict(emiscode=13, toilet_usable=6, toilets_total=7)]), 1),
    ('In this test we test not operator. Two School and BasicFacilities '
     'records exist in database. Both records fulfill criteria but dist_id of '
     'one record is different than given dist_id so method should return 1.',
     dict(criteria=dict(field_model='BasicFacilities', value=50,
                        operator=constants.NOT_OP, field_name='toilet_usable',
                        total_field_name='toilets_total'),
          dist_id=1, count_all=False,
          school_data=[dict(emiscode=12, dist_id=1),
                       dict(emiscode=13, dist_id=2)],
          basic_facility_data=[
              dict(emiscode=12, toilet_usable=5, toilets_total=8),
              dict(emiscode=13, toilet_usable=2, toilets_total=6)]), 1)])
def test_get_join_table_percentage_count(description, test_input, expected,
                                         session):
    """In this test, we add record in School and BasicFacilities table according
    to test data and verify test that count returned by method
    get_join_table_percentage_count() is according to test data."""

    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facility_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_join_table_percentage_count(
        test_input['criteria'], test_input['dist_id'], test_input['count_all'])
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1),
                       dict(head_charge=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1),
                       dict(head_charge=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1),
                       dict(dist_id=1, head_charge=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1),
                       dict(dist_id=2, head_charge=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1),
                       dict(dist_id=1, head_charge=1)]), 2)])
def test_get_schools_with_permanent_head_charge(description, test_input,
                                                expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_permanent_head_charge() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_permanent_head_charge(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1),
                       dict(head_charge=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=2),
                       dict(head_charge=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1),
                       dict(dist_id=1, head_charge=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=2),
                       dict(dist_id=2, head_charge=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=2),
                       dict(dist_id=1, head_charge=2)]), 2)])
def test_get_schools_with_additional_head_charge(description, test_input,
                                                 expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_additional_head_charge() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_additional_head_charge(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=1),
                       dict(head_charge=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(head_charge=3),
                       dict(head_charge=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=1),
                       dict(dist_id=1, head_charge=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=3),
                       dict(dist_id=2, head_charge=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, head_charge=3),
                       dict(dist_id=1, head_charge=3)]), 2)])
def test_get_schools_with_lookafter_head_charge(description, test_input,
                                                expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_lookafter_head_charge() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_lookafter_head_charge(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=2, school_status=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=1)]), 2)])
def test_get_functional_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_functional_schools() is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_functional_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=2),
                       dict(school_status=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2),
                       dict(dist_id=2, school_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2),
                       dict(dist_id=1, school_status=2)]), 2)])
def test_get_non_functional_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_non_functional_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_non_functional_schools(test_input['dist_id'],
                                                         count=False)
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=4),
                       dict(school_status=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=4),
                       dict(dist_id=2, school_status=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=4),
                       dict(dist_id=1, school_status=4)]), 2)])
def test_get_denotified_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_denotified_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_denotified_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=3),
                       dict(school_status=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=3),
                       dict(dist_id=2, school_status=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=3),
                       dict(dist_id=1, school_status=3)]), 2)])
def test_get_merged_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_merged_schools is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_merged_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=5)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_status=1),
                       dict(school_status=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_status=5),
                       dict(school_status=5)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=5)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=1),
                       dict(dist_id=1, school_status=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=5),
                       dict(dist_id=2, school_status=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_status=5),
                       dict(dist_id=1, school_status=5)]), 2)])
def test_get_consolidated_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_consolidated_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_consolidated_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(medium=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(medium=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(medium=1),
                       dict(medium=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(medium=1),
                       dict(medium=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1),
                       dict(dist_id=1, medium=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1),
                       dict(dist_id=2, medium=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1),
                       dict(dist_id=1, medium=1)]), 2)])
def test_get_english_medium_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_english_medium_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_english_medium_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(medium=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(medium=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(medium=2),
                       dict(medium=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(medium=2),
                       dict(medium=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=2),
                       dict(dist_id=1, medium=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=2),
                       dict(dist_id=2, medium=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=2),
                       dict(dist_id=1, medium=2)]), 2)])
def test_get_urdu_medium_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_urdu_medium_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_urdu_medium_schools(test_input['dist_id'],
                                                      count=False)
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(medium=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(medium=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(medium=3),
                       dict(medium=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(medium=3),
                       dict(medium=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=3),
                       dict(dist_id=1, medium=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=3),
                       dict(dist_id=3, medium=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, medium=3),
                       dict(dist_id=1, medium=3)]), 2)])
def test_get_both_urdu_and_english_medium_schools(description, test_input,
                                                  expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_both_urdu_and_english_medium_schools is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_both_urdu_and_english_medium_schools(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=1),
                       dict(school_shift=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=1),
                       dict(school_shift=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=1),
                       dict(dist_id=1, school_shift=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=1),
                       dict(dist_id=2, school_shift=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=1),
                       dict(dist_id=1, school_shift=1)]), 2)])
def test_get_morning_shift_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_morning_shift_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_morning_shift_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=2),
                       dict(school_shift=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_shift=2),
                       dict(school_shift=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=2),
                       dict(dist_id=1, school_shift=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=2),
                       dict(dist_id=2, school_shift=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_shift=2),
                       dict(dist_id=1, school_shift=2)]), 2)])
def test_get_evening_shift_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_evening_shift_schools is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_evening_shift_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_location=1),
                       dict(school_location=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=1),
                       dict(school_location=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=1),
                       dict(dist_id=1, school_location=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=1),
                       dict(dist_id=2, school_location=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=1),
                       dict(dist_id=1, school_location=1)]), 2)])
def test_get_urban_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_urban_schools is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_urban_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_location=2),
                       dict(school_location=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_location=2),
                       dict(school_location=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=2),
                       dict(dist_id=1, school_location=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=2),
                       dict(dist_id=2, school_location=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_location=2),
                       dict(dist_id=1, school_location=2)]), 2)])
def test_get_rural_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_rural_schools is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_rural_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1),
                       dict(non_func_reason=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1),
                       dict(non_func_reason=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=1, non_func_reason=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=2, non_func_reason=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=1, non_func_reason=1)]), 2)])
def test_get_schools_closed_due_to_teachers_nonavailability(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_closed_due_to_teachers_
    nonavailability() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_closed_due_to_teachers_nonavailability(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1),
                       dict(non_func_reason=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=2),
                       dict(non_func_reason=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=1, non_func_reason=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=2),
                       dict(dist_id=2, non_func_reason=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=2),
                       dict(dist_id=1, non_func_reason=2)]), 2)])
def test_get_schools_closed_due_to_students_nonavailability(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_closed_due_to_students_
    nonavailability() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_closed_due_to_students_nonavailability(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1),
                       dict(non_func_reason=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=3),
                       dict(non_func_reason=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=1, non_func_reason=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=3),
                       dict(dist_id=2, non_func_reason=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=3),
                       dict(dist_id=1, non_func_reason=3)]), 2)])
def test_get_schools_closed_due_to_building_nonavailability(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_closed_due_to_building_
    nonavailability() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_closed_due_to_building_nonavailability(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=1),
                       dict(non_func_reason=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(non_func_reason=4),
                       dict(non_func_reason=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=1),
                       dict(dist_id=1, non_func_reason=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=4),
                       dict(dist_id=2, non_func_reason=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, non_func_reason=4),
                       dict(dist_id=1, non_func_reason=4)]), 2)])
def test_get_schools_closed_due_to_building_occupied(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_closed_due_to_building_occupied()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_closed_due_to_building_occupied(
        test_input['dist_id'], count=False)
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=1),
                       dict(gender_register=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=1),
                       dict(gender_register=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=1),
                       dict(dist_id=1, gender_register=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=1),
                       dict(dist_id=2, gender_register=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=1),
                       dict(dist_id=1, gender_register=1)]), 2)])
def test_get_schools_only_for_boys(description, test_input,
                                   expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_only_for_boys() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_only_for_boys(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=1),
                       dict(gender_register=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(gender_register=2),
                       dict(gender_register=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=1),
                       dict(dist_id=1, gender_register=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=2),
                       dict(dist_id=2, gender_register=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_register=2),
                       dict(dist_id=1, gender_register=2)]), 2)])
def test_get_schools_only_for_girls(description, test_input,
                                    expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_only_for_girls() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_only_for_girls(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1),
                       dict(gender_studying=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1),
                       dict(gender_studying=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=1),
                       dict(dist_id=1, gender_studying=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=1),
                       dict(dist_id=2, gender_studying=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=1),
                       dict(dist_id=1, gender_studying=1)]), 2)])
def test_get_schools_only_boys_studying(description, test_input,
                                        expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_only_boys_studying() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_only_boys_studying(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1),
                       dict(gender_studying=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=2),
                       dict(gender_studying=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=1),
                       dict(dist_id=1, gender_studying=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=2),
                       dict(dist_id=2, gender_studying=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=2),
                       dict(dist_id=1, gender_studying=2)]), 2)])
def test_get_schools_only_girls_studying(description, test_input,
                                         expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_only_girls_studying() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_only_girls_studying(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=1),
                       dict(gender_studying=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(gender_studying=3),
                       dict(gender_studying=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3),
                       dict(dist_id=1, gender_studying=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3),
                       dict(dist_id=2, gender_studying=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, gender_studying=3),
                       dict(dist_id=1, gender_studying=3)]), 2)])
def test_get_schools_both_girl_and_boys_are_studying(description, test_input,
                                                     expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_both_girl_and_boys_are_studying()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_both_girl_and_boys_are_studying(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='Primary')]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque')]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='Primary')]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='sMosque')]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle')]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='sMosque')]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='sMosque'),
                       dict(dist_id=1, school_level='Primary')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='sMosque'),
                       dict(dist_id=2, school_level='sMosque')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='sMosque'),
                       dict(dist_id=1, school_level='sMosque')]), 2)])
def test_get_mosque_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_mosque_schools() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_mosque_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque')]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='Primary')]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='Primary')]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='Primary'),
                       dict(school_level='Primary')]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle')]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary')]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='sMosque'),
                       dict(dist_id=1, school_level='Primary')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary'),
                       dict(dist_id=2, school_level='Primary')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary'),
                       dict(dist_id=1, school_level='Primary')]), 2)])
def test_get_primary_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_primary_schools() is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_primary_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque')]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='Middle')]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='Middle')]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='Middle'),
                       dict(school_level='Middle')]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary')]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle')]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle'),
                       dict(dist_id=1, school_level='sMosque')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle'),
                       dict(dist_id=2, school_level='Middle')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Middle'),
                       dict(dist_id=1, school_level='Middle')]), 2)])
def test_get_middle_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_middle_schools() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_middle_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque')]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='High')]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='High')]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='High'),
                       dict(school_level='High')]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary')]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='High')]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='High'),
                       dict(dist_id=1, school_level='sMosque')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='High'),
                       dict(dist_id=2, school_level='High')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='High'),
                       dict(dist_id=1, school_level='High')]), 2)])
def test_get_high_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_high_schools() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_high_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque')]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='H.Sec.')]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_level='sMosque'),
                       dict(school_level='H.Sec.')]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_level='H.Sec.'),
                       dict(school_level='H.Sec.')]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='Primary')]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='H.Sec.')]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='H.Sec.'),
                       dict(dist_id=1, school_level='sMosque')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='H.Sec.'),
                       dict(dist_id=2, school_level='H.Sec.')]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_level='H.Sec.'),
                       dict(dist_id=1, school_level='H.Sec.')]), 2)])
def get_higher_secondary_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_higher_secondary_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_higher_secondary_schools(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=2, school_type=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=1)]), 2)])
def test_get_internet_in_community_model_schools(description, test_input, expected,
                                                 session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_community_model_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_community_model_schools(test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=2),
                       dict(school_type=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2),
                       dict(dist_id=2, school_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2),
                       dict(dist_id=1, school_type=2)]), 2)])
def test_get_junior_model_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_junior_model_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_junior_model_schools(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=3),
                       dict(school_type=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=3),
                       dict(dist_id=2, school_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=3),
                       dict(dist_id=1, school_type=3)]), 2)])
def test_get_pilot_secondary_schools(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_pilot_secondary_schools is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_pilot_secondary_schools(test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=4),
                       dict(school_type=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=4),
                       dict(dist_id=2, school_type=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=4),
                       dict(dist_id=1, school_type=4)]), 2)])
def test_get_comprehensive_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_comprehensive_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_comprehensive_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=5)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=5),
                       dict(school_type=5)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=5)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=5),
                       dict(dist_id=2, school_type=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=5),
                       dict(dist_id=1, school_type=5)]), 2)])
def test_get_technical_high_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_technical_high_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_technical_high_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=6)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=6)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=6),
                       dict(school_type=6)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=6)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=6)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=6),
                       dict(dist_id=2, school_type=6)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=6),
                       dict(dist_id=1, school_type=6)]), 2)])
def test_get_model_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_model_schools() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_model_schools(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=7)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(school_type=1),
                       dict(school_type=7)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(school_type=7),
                       dict(school_type=7)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=7)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=1),
                       dict(dist_id=1, school_type=7)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=7),
                       dict(dist_id=2, school_type=7)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, school_type=7),
                       dict(dist_id=1, school_type=7)]), 2)])
def test_get_local_government_schools(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_local_government_schools() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_local_government_schools(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=1),
                       dict(bldg_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=1),
                       dict(bldg_status=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=1),
                       dict(dist_id=1, bldg_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=1),
                       dict(dist_id=2, bldg_status=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=1),
                       dict(dist_id=1, bldg_status=1)]), 2)])
def test_get_schools_with_building(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building(test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=1),
                       dict(bldg_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_status=2),
                       dict(bldg_status=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=1),
                       dict(dist_id=1, bldg_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=2),
                       dict(dist_id=2, bldg_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_status=2),
                       dict(dist_id=1, bldg_status=2)]), 2)])
def test_get_schools_without_building(description, test_input, expected,
                                      session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_building() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_without_building(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=2, bldg_ownship=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=1)]), 2)])
def test_get_schools_with_building_owned_by_education_department(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_owned_by_education_
    department() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_owned_by_education_department(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=2),
                       dict(bldg_ownship=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2),
                       dict(dist_id=2, bldg_ownship=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2),
                       dict(dist_id=1, bldg_ownship=2)]), 2)])
def test_get_schools_with_building_owned_by_another_govt_school(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_owned_by_another_
    govt_school() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_owned_by_another_govt_school(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=3),
                       dict(bldg_ownship=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=3),
                       dict(dist_id=2, bldg_ownship=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=3),
                       dict(dist_id=1, bldg_ownship=3)]), 2)])
def test_get_schools_with_building_is_on_lease(description, test_input,
                                               expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_is_on_lease() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_building_is_on_lease(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=4),
                       dict(bldg_ownship=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=4),
                       dict(dist_id=2, bldg_ownship=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=4),
                       dict(dist_id=1, bldg_ownship=4)]), 2)])
def test_get_schools_with_building_provided_by_local_population(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_provided_by_local_
    population() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_provided_by_local_population(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=5)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=5),
                       dict(bldg_ownship=5)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=5)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=5),
                       dict(dist_id=2, bldg_ownship=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=5),
                       dict(dist_id=1, bldg_ownship=5)]), 2)])
def test_get_schools_with_building_is_owned_by_municipal_corporation(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_is_owned_by_
    municipal_corporation() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (models.School.
        get_schools_with_building_is_owned_by_municipal_corporation(
        test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=6)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=6)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=6),
                       dict(bldg_ownship=6)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=6)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=6)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=6),
                       dict(dist_id=2, bldg_ownship=6)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=6),
                       dict(dist_id=1, bldg_ownship=6)]), 2)])
def test_get_schools_with_building_provided_by_school_council(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_provided_by_school_
    council() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_provided_by_school_council(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=7)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=7)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=7),
                       dict(bldg_ownship=7)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=7)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=7)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=7),
                       dict(dist_id=2, bldg_ownship=7)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=7),
                       dict(dist_id=1, bldg_ownship=7)]), 2)])
def test_get_schools_building_owned_by_other_govt_institute_than_municipal_corporation(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_building_owned_by_other_govt_
    institute_than_municipal_corporation() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (models.School.
        get_schools_building_owned_by_other_govt_institute_than_municipal_corporation(
        test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=8)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=1),
                       dict(bldg_ownship=8)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_ownship=8),
                       dict(bldg_ownship=8)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=8)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=1),
                       dict(dist_id=1, bldg_ownship=8)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=8),
                       dict(dist_id=2, bldg_ownship=8)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_ownship=8),
                       dict(dist_id=1, bldg_ownship=8)]), 2)])
def test_get_schools_running_in_mosque(description, test_input, expected,
                                       session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_running_in_mosque() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_running_in_mosque(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(place_status=1),
                       dict(place_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=1),
                       dict(place_status=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=1),
                       dict(dist_id=1, place_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=1),
                       dict(dist_id=2, place_status=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=1),
                       dict(dist_id=1, place_status=1)]), 2)])
def test_get_schools_running_in_a_place_where_government_created_them(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_running_in_a_place_where_
    government_created_them() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (models.School.
        get_schools_running_in_a_place_where_government_created_them(
        test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(place_status=1),
                       dict(place_status=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(place_status=2),
                       dict(place_status=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=1),
                       dict(dist_id=1, place_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=2),
                       dict(dist_id=2, place_status=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, place_status=2),
                       dict(dist_id=1, place_status=2)]), 2)])
def test_get_schools_not_running_in_a_place_where_government_created_them(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_not_running_in_a_place_where_
    government_created_them() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (models.School.
        get_schools_not_running_in_a_place_where_government_created_them(
        test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1),
                       dict(construct_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1),
                       dict(construct_type=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1),
                       dict(dist_id=1, construct_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1),
                       dict(dist_id=2, construct_type=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1),
                       dict(dist_id=1, construct_type=1)]), 2)])
def test_get_schools_building_construction_type_is_mud(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_building_construction_type_is_mud()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (models.School.get_schools_building_construction_type_is_mud(
        test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1),
                       dict(construct_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=2),
                       dict(construct_type=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1),
                       dict(dist_id=1, construct_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=2),
                       dict(dist_id=2, construct_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=2),
                       dict(dist_id=1, construct_type=2)]), 2)])
def test_get_schools_building_construction_type_is_concrete(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_building_construction_type_is_
    concrete() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_building_construction_type_is_concrete(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=1),
                       dict(construct_type=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(construct_type=3),
                       dict(construct_type=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=1),
                       dict(dist_id=1, construct_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=3),
                       dict(dist_id=2, construct_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, construct_type=3),
                       dict(dist_id=1, construct_type=3)]), 2)])
def test_get_schools_building_construction_type_is_both_concrete_and_mud(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_building_construction_type_is_
    both_concrete_and_mud() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_building_construction_type_is_both_concrete_and_mud(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=2, bldg_condition=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=1)]), 2)])
def test_get_schools_with_stable_building_condition(description, test_input,
                                                    expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_stable_building_condition()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_stable_building_condition(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=2),
                       dict(bldg_condition=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2),
                       dict(dist_id=2, bldg_condition=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2),
                       dict(dist_id=1, bldg_condition=2)]), 2)])
def test_get_schools_with_building_require_partial_renovation(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_require_partial_
    renovation() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_require_partial_renovation(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=3),
                       dict(bldg_condition=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=3),
                       dict(dist_id=2, bldg_condition=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=3),
                       dict(dist_id=1, bldg_condition=3)]), 2)])
def test_get_schools_with_building_require_full_renovation(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_require_full_
    renovation() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_with_building_require_full_renovation(
        test_input['dist_id'], count=False)
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=4),
                       dict(bldg_condition=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=4),
                       dict(dist_id=2, bldg_condition=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=4),
                       dict(dist_id=1, bldg_condition=4)]), 2)])
def test_get_schools_with_building_condition_fully_dangerous(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_condition_fully_
    dangerous() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_condition_fully_dangerous(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=5)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=1),
                       dict(bldg_condition=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(bldg_condition=5),
                       dict(bldg_condition=5)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=5)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=1),
                       dict(dist_id=1, bldg_condition=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=5),
                       dict(dist_id=2, bldg_condition=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(dist_id=1, bldg_condition=5),
                       dict(dist_id=1, bldg_condition=5)]), 2)])
def test_get_schools_with_building_condition_partially_dangerous(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_building_condition_partially_
    dangerous() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = (
        models.School.get_schools_with_building_condition_partially_dangerous(
            test_input['dist_id'], count=False))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=1)]), 2)])
def test_get_schools_with_drinking_water_facilities_available(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_drinking_water_facilities_
    available() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_drinking_water_facilities_available(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2),
                                 dict(emiscode=2, drink_water=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2),
                                 dict(emiscode=2, drink_water=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=2),
                                 dict(emiscode=2, drink_water=2)]), 2)])
def test_get_schools_without_drinking_water_facilities(description, test_input,
                                                       expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_drinking_water_facilities()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_drinking_water_facilities(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=3),
                                 dict(emiscode=2, drink_water=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=1),
                                 dict(emiscode=2, drink_water=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water=3),
                                 dict(emiscode=2, drink_water=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water=3),
                                 dict(emiscode=2, drink_water=3)]), 2)])
def test_get_schools_with_drinking_water_facilities_not_working(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_drinking_water_facilities_
    not_working() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_drinking_water_facilities_not_working(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=1)]), 2)])
def test_get_schools_with_drinking_water_source_is_well(description, test_input,
                                                        expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_drinking_water_source_is_well
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_drinking_water_source_is_well(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2),
                                 dict(emiscode=2, drink_water_type=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2),
                                 dict(emiscode=2, drink_water_type=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=2),
                                 dict(emiscode=2, drink_water_type=2)]), 2)])
def test_get_schools_where_drinking_water_source_is_hand_pump(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_where_drinking_water_source_is_
    hand_pump() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_where_drinking_water_source_is_hand_pump(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=3),
                                 dict(emiscode=2, drink_water_type=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=3),
                                 dict(emiscode=2, drink_water_type=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=3),
                                 dict(emiscode=2, drink_water_type=3)]), 2)])
def test_get_schools_where_drinking_water_source_is_water_pump(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_where_drinking_water_source_is_
    water_pump() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_where_drinking_water_source_is_water_pump(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=4)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=4)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=4),
                                 dict(emiscode=2, drink_water_type=4)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=4)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=4),
                                 dict(emiscode=2, drink_water_type=4)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=4),
                                 dict(emiscode=2, drink_water_type=4)]), 2)])
def test_get_schools_where_drinking_water_source_is_govt_null(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_where_drinking_water_source_is_
    govt_null() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_where_drinking_water_source_is_govt_null(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=5)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=5)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=5),
                                 dict(emiscode=2, drink_water_type=5)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=5)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=1),
                                 dict(emiscode=2, drink_water_type=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=5),
                                 dict(emiscode=2, drink_water_type=5)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, drink_water_type=5),
                                 dict(emiscode=2, drink_water_type=5)]), 2)])
def test_get_schools_where_drinking_water_source_is_other(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_where_drinking_water_source_is_
    other) is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_where_drinking_water_source_is_other(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=1)]), 2)])
def test_get_schools_with_electricity(description, test_input, expected,
                                      session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_electricity() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_electricity(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=2),
                                 dict(emiscode=2, electricity=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=2),
                                 dict(emiscode=2, electricity=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=2),
                                 dict(emiscode=2, electricity=2)]), 2)])
def test_get_schools_with_no_electricity(description, test_input, expected,
                                         session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_no_electricity() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_no_electricity(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=3),
                                 dict(emiscode=2, electricity=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=1),
                                 dict(emiscode=2, electricity=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity=3),
                                 dict(emiscode=2, electricity=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity=3),
                                 dict(emiscode=2, electricity=3)]), 2)])
def test_get_schools_with_electricity_not_working(description, test_input,
                                                  expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_electricity_not_working() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_electricity_not_working(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=1)]), 2)])
def test_get_schools_without_electricity_due_to_bill_not_paid(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_electricity_due_to_bill_
    not_paid() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_electricity_due_to_bill_not_paid(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2),
                                 dict(emiscode=2, electricity_reasons=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2),
                                 dict(emiscode=2, electricity_reasons=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=2),
                                 dict(emiscode=2, electricity_reasons=2)]), 2)])
def test_get_schools_with_no_electricity_due_to_faulty_wiring(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_no_electricity_due_to_faulty_
    wiring() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_no_electricity_due_to_faulty_wiring(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=3),
                                 dict(emiscode=2, electricity_reasons=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=1),
                                 dict(emiscode=2, electricity_reasons=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=3),
                                 dict(emiscode=2, electricity_reasons=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, electricity_reasons=3),
                                 dict(emiscode=2, electricity_reasons=3)]), 2)])
def test_get_schools_with_no_electricity_due_to_no_connection(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_no_electricity_due_to_no_
    connection() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_no_electricity_due_to_no_connection(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=1)]), 2)])
def test_get_schools_with_toilets(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_toilets() is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_toilets(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=2),
                                 dict(emiscode=2, toilets=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=2),
                                 dict(emiscode=2, toilets=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=2),
                                 dict(emiscode=2, toilets=2)]), 2)])
def test_get_schools_with_no_toilets(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_no_toilets() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_no_toilets(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=3),
                                 dict(emiscode=2, toilets=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=1),
                                 dict(emiscode=2, toilets=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, toilets=3),
                                 dict(emiscode=2, toilets=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, toilets=3),
                                 dict(emiscode=2, toilets=3)]), 2)])
def test_get_schools_with_nonfunctional_toilets(description, test_input,
                                                expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_nonfunctional_toilets() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_nonfunctional_toilets(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=1)]), 2)])
def test_get_schools_with_boundary_wall(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_boundary_wall() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_boundary_wall(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2),
                                 dict(emiscode=2, boundary_wall=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=1),
                                 dict(emiscode=2, boundary_wall=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2),
                                 dict(emiscode=2, boundary_wall=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, boundary_wall=2),
                                 dict(emiscode=2, boundary_wall=2)]), 2)])
def test_get_schools_without_boundary_wall(description, test_input, expected,
                                           session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_boundary_wall() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_boundary_wall(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=1)]), 2)])
def test_get_schools_with_complete_boundary_wall(description, test_input,
                                                 expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_complete_boundary_wall() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_complete_boundary_wall(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2),
                                 dict(emiscode=2, bwall_complete=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2),
                                 dict(emiscode=2, bwall_complete=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=2),
                                 dict(emiscode=2, bwall_complete=2)]), 2)])
def test_get_schools_with_incomplete_boundary_wall(description, test_input,
                                                   expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_incomplete_boundary_wall() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_incomplete_boundary_wall(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=3)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=3)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=3),
                                 dict(emiscode=2, bwall_complete=3)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=3)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=1),
                                 dict(emiscode=2, bwall_complete=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=3),
                                 dict(emiscode=2, bwall_complete=3)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, bwall_complete=3),
                                 dict(emiscode=2, bwall_complete=3)]), 2)])
def test_get_schools_with_boundary_wall_in_bad_condition(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_boundary_wall_in_bad_
    condition() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_boundary_wall_in_bad_condition(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=1)]), 2)])
def test_get_schools_with_main_gate(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_main_gate() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_main_gate(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2),
                                 dict(emiscode=2, main_gate=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=1),
                                 dict(emiscode=2, main_gate=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2),
                                 dict(emiscode=2, main_gate=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, main_gate=2),
                                 dict(emiscode=2, main_gate=2)]), 2)])
def test_get_schools_without_main_gate(description, test_input, expected,
                                       session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_main_gate() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_main_gate(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=1)]), 2)])
def test_get_schools_with_sewerage_system(description, test_input, expected,
                                          session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_sewerage_system() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_sewerage_system(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2),
                                 dict(emiscode=2, sewerage=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          basic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=1),
                                 dict(emiscode=2, sewerage=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2),
                                 dict(emiscode=2, sewerage=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          basic_facilities_data=[dict(emiscode=1, sewerage=2),
                                 dict(emiscode=2, sewerage=2)]), 2)])
def test_get_schools_without_sewerage_system(description, test_input, expected,
                                             session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_sewerage_system() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['basic_facilities_data']:
        basic_facility = models.BasicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_sewerage_system(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=1)]), 2)])
def test_get_schools_with_playground(description, test_input, expected,
                                     session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_playground() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_playground(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2),
                                  dict(emiscode=2, play_ground=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=1),
                                  dict(emiscode=2, play_ground=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2),
                                  dict(emiscode=2, play_ground=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, play_ground=2),
                                  dict(emiscode=2, play_ground=2)]), 2)])
def test_get_schools_without_playground(description, test_input, expected,
                                        session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_playground() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_playground(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, circket=1),
                                  dict(emiscode=2, circket=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, circket=1),
                                  dict(emiscode=2, circket=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=1),
                                  dict(emiscode=2, circket=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, circket=1),
                                  dict(emiscode=2, circket=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, circket=1),
                                  dict(emiscode=2, circket=1)]), 2)])
def test_get_schools_with_facilities_for_cricket(description, test_input,
                                                 expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_cricket() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_cricket(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, football=1),
                                  dict(emiscode=2, football=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, football=1),
                                  dict(emiscode=2, football=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=1),
                                  dict(emiscode=2, football=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, football=1),
                                  dict(emiscode=2, football=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, football=1),
                                  dict(emiscode=2, football=1)]), 2)])
def test_get_schools_with_facilities_for_football(description, test_input,
                                                  expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_football() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_football(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, hockey=1),
                                  dict(emiscode=2, hockey=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, hockey=1),
                                  dict(emiscode=2, hockey=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=1),
                                  dict(emiscode=2, hockey=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, hockey=1),
                                  dict(emiscode=2, hockey=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, hockey=1),
                                  dict(emiscode=2, hockey=1)]), 2)])
def test_get_schools_with_facilities_for_hockey(description, test_input,
                                                expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_hockey() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_hockey(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, badminton=1),
                                  dict(emiscode=2, badminton=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, badminton=1),
                                  dict(emiscode=2, badminton=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=1),
                                  dict(emiscode=2, badminton=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, badminton=1),
                                  dict(emiscode=2, badminton=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, badminton=1),
                                  dict(emiscode=2, badminton=1)]), 2)])
def test_get_schools_with_facilities_for_badminton(description, test_input,
                                                   expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_badminton() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_badminton(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1),
                                  dict(emiscode=2, volleyball=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1),
                                  dict(emiscode=2, volleyball=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1),
                                  dict(emiscode=2, volleyball=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1),
                                  dict(emiscode=2, volleyball=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, volleyball=1),
                                  dict(emiscode=2, volleyball=1)]), 2)])
def test_get_schools_with_facilities_for_volleyball(description, test_input,
                                                    expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_volleyball() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_volleyball(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1),
                                  dict(emiscode=2, table_tennis=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1),
                                  dict(emiscode=2, table_tennis=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1),
                                  dict(emiscode=2, table_tennis=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1),
                                  dict(emiscode=2, table_tennis=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, table_tennis=1),
                                  dict(emiscode=2, table_tennis=1)]), 2)])
def test_get_schools_with_facilities_for_table_tennis(description, test_input,
                                                      expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_table_tennis()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_table_tennis(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, other=1),
                                  dict(emiscode=2, other=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, other=1),
                                  dict(emiscode=2, other=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=1),
                                  dict(emiscode=2, other=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[dict(emiscode=1, other=1),
                                  dict(emiscode=2, other=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[dict(emiscode=1, other=1),
                                  dict(emiscode=2, other=1)]), 2)])
def test_get_schools_with_facilities_for_other_sports(description, test_input,
                                                      expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_facilities_for_other_sports()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_facilities_for_other_sports(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=1)]), 2)])
def test_get_schools_with_library(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_library() is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_library(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=2),
                                    dict(emiscode=2, library=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=1),
                                    dict(emiscode=2, library=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, library=2),
                                    dict(emiscode=2, library=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, library=2),
                                    dict(emiscode=2, library=2)]), 2)])
def test_get_schools_without_library(description, test_input, expected,
                                     session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_library() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_library(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=1)]), 2)])
def test_get_schools_with_lab(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_lab() is according to test
    data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_lab(test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2),
                                    dict(emiscode=2, lab_exist=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=1),
                                    dict(emiscode=2, lab_exist=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2),
                                    dict(emiscode=2, lab_exist=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, lab_exist=2),
                                    dict(emiscode=2, lab_exist=2)]), 2)])
def test_get_schools_without_lab(description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_lab() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_lab(test_input['dist_id'],
                                                      count=False)
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=1)]), 2)])
def test_get_schools_with_physics_lab(description, test_input, expected,
                                      session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_physics_lab() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_physics_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2),
                                    dict(emiscode=2, physics_lab=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=1),
                                    dict(emiscode=2, physics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2),
                                    dict(emiscode=2, physics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_lab=2),
                                    dict(emiscode=2, physics_lab=2)]), 2)])
def test_get_schools_without_physics_lab(description, test_input, expected,
                                         session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_physics_lab() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_physics_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=1)]), 2)])
def test_get_schools_with_biology_lab(description, test_input, expected,
                                      session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_biology_lab() is according to
    test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_biology_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2),
                                    dict(emiscode=2, biology_lab=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=1),
                                    dict(emiscode=2, biology_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2),
                                    dict(emiscode=2, biology_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_lab=2),
                                    dict(emiscode=2, biology_lab=2)]), 2)])
def test_get_schools_without_biology_lab(description, test_input, expected,
                                         session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_biology_lab() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_biology_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=1)]), 2)])
def test_get_schools_with_chemistry_lab(description, test_input, expected,
                                        session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_chemistry_lab() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_chemistry_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2),
                                    dict(emiscode=2, chemistry_lab=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=1),
                                    dict(emiscode=2, chemistry_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2),
                                    dict(emiscode=2, chemistry_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_lab=2),
                                    dict(emiscode=2, chemistry_lab=2)]), 2)])
def test_get_schools_without_chemistry_lab(description, test_input, expected,
                                           session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_chemistry_lab() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_chemistry_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=1)]), 2)])
def test_get_schools_with_home_economics_lab(description, test_input, expected,
                                             session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_home_economics_lab() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_home_economics_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2),
                                    dict(emiscode=2, homeconomics_lab=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=1),
                                    dict(emiscode=2, homeconomics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2),
                                    dict(emiscode=2, homeconomics_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, homeconomics_lab=2),
                                    dict(emiscode=2, homeconomics_lab=2)]), 2)])
def test_get_schools_without_home_economics_lab(description, test_input,
                                                expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_home_economics_lab() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_without_home_economics_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=1)]), 2)])
def test_get_schools_with_combine_lab_for_science_subjects(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_combine_lab_for_science_
    subjects() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_schools_with_combine_lab_for_science_subjects(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2),
                                    dict(emiscode=2, combine_lab=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=1),
                                    dict(emiscode=2, combine_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2),
                                    dict(emiscode=2, combine_lab=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_lab=2),
                                    dict(emiscode=2, combine_lab=2)]), 2)])
def test_get_schools_without_combine_lab_for_science_subjects(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_combine_lab_for_science_
    subjects() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_combine_lab_for_science_subjects(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=1)]), 2)])
def test_get_schools_with_enough_instrument_for_physics_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_enough_instrument_for_physics_
    lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_enough_instrument_for_physics_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2),
                                    dict(emiscode=2, physics_instrument=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=1),
                                    dict(emiscode=2, physics_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2),
                                    dict(emiscode=2, physics_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, physics_instrument=2),
                                    dict(emiscode=2, physics_instrument=2)]), 2)])
def test_get_schools_without_enough_instrument_for_physics_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_enough_instrument_for_
    physics_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_enough_instrument_for_physics_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=1)]), 2)])
def test_get_schools_with_enough_instrument_for_biology_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_enough_instrument_for_biology_
    lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_enough_instrument_for_biology_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2),
                                    dict(emiscode=2, biology_instrument=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=1),
                                    dict(emiscode=2, biology_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2),
                                    dict(emiscode=2, biology_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, biology_instrument=2),
                                    dict(emiscode=2, biology_instrument=2)]), 2)])
def test_get_schools_without_enough_instrument_for_biology_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_enough_instrument_for_
    biology_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_enough_instrument_for_biology_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2)]),
     0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1)]),
     1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=1)]),
     2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2)]),
     0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1)]),
     1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=1)]),
     1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=1)]),
     2)])
def test_get_schools_with_enough_instrument_for_chemistry_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_enough_instrument_for_chemistry_
    lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_enough_instrument_for_chemistry_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1)]),
     0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2)]),
     1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1)]),
     0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2)]),
     1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=1),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, chemistry_instrument=2),
                                    dict(emiscode=2, chemistry_instrument=2)]),
     2)])
def test_get_schools_without_enough_instrument_for_chemistry_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_enough_instrument_for_
    chemistry_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_enough_instrument_for_chemistry_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=1)]), 2)])
def test_get_schools_with_enough_instrument_for_home_economics_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_enough_instrument_for_home_economics_
    lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_enough_instrument_for_home_economics_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2),
                                    dict(emiscode=2, home_instrument=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=1),
                                    dict(emiscode=2, home_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2),
                                    dict(emiscode=2, home_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, home_instrument=2),
                                    dict(emiscode=2, home_instrument=2)]), 2)])
def test_get_schools_without_enough_instrument_for_home_economics_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_enough_instrument_for_
    home_economics_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_enough_instrument_for_home_economics_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=1)]), 2)])
def test_get_schools_with_enough_instrument_for_combine_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_with_enough_instrument_for_combine_
    lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_with_enough_instrument_for_combine_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2),
                                    dict(emiscode=2, combine_instrument=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=1),
                                    dict(emiscode=2, combine_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2),
                                    dict(emiscode=2, combine_instrument=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, combine_instrument=2),
                                    dict(emiscode=2, combine_instrument=2)]), 2)])
def test_get_schools_without_enough_instrument_for_combine_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_enough_instrument_for_
    combine_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_enough_instrument_for_combine_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=1)]), 2)])
def test_get_morning_shift_schools_with_computer_lab(description, test_input,
                                                     expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_morning_shift_schools_with_computer_lab()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_morning_shift_schools_with_computer_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2),
                                    dict(emiscode=2, com_lab_morning=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=1),
                                    dict(emiscode=2, com_lab_morning=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2),
                                    dict(emiscode=2, com_lab_morning=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_morning=2),
                                    dict(emiscode=2, com_lab_morning=2)]), 2)])
def test_get_morning_shift_schools_without_computer_lab(description, test_input,
                                                        expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_morning_shift_schools_without_computer_lab()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_morning_shift_schools_without_computer_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=1)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=1)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=1)]), 2)])
def test_get_evening_shift_schools_with_computer_lab(description, test_input,
                                                     expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_evening_shift_schools_with_computer_lab()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_evening_shift_schools_with_computer_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=2)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2),
                                    dict(emiscode=2, com_lab_evening=2)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=1),
                                    dict(emiscode=2, com_lab_evening=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2),
                                    dict(emiscode=2, com_lab_evening=2)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[dict(emiscode=1, com_lab_evening=2),
                                    dict(emiscode=2, com_lab_evening=2)]), 2)])
def test_get_evening_shift_schools_without_computer_lab(description, test_input,
                                                        expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_evening_shift_schools_without_computer_lab()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = models.School.get_evening_shift_schools_without_computer_lab(
        test_input['dist_id'])
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 2)])
def test_get_morning_shift_schools_with_internet_in_computer_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_morning_shift_schools_with_internet_in_
    computer_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_morning_shift_schools_with_internet_in_computer_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING),
              dict(emiscode=2,
                   internet_morning=constants.NO_INTERNET_ACCESS_MORNING)]),
     2)])
def test_get_morning_shift_schools_without_internet_in_computer_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_morning_shift_schools_without_internet_in_
    computer_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_morning_shift_schools_without_internet_in_computer_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 2)])
def test_get_evening_shift_schools_with_internet_in_computer_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_evening_shift_schools_with_internet_in_
    computer_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_evening_shift_schools_with_internet_in_computer_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING),
              dict(emiscode=2,
                   internet_evening=constants.NO_INTERNET_ACCESS_EVENING)]),
     2)])
def test_get_evening_shift_schools_without_internet_in_computer_lab(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_evening_shift_schools_without_internet_in_
    computer_lab() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_evening_shift_schools_without_internet_in_computer_lab(
            test_input['dist_id']))
    assert len(retrieved) == expected

