"""Model School unit tests. This file contains test for methods in School
model."""
import math

import pytest

from schoolCensus import constants
from schoolCensus.school_models import models


@pytest.mark.usefixtures('session')
class TestSchoolModelMethodGetDistricts:
    """School model method get_districts tests."""

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
        ('In this test one districts record exist in database so method should '
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

