import math

import pytest

from schoolCensus import constants
from schoolCensus.school_models import models


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(dist_id=1, new_construct_year=3)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1,
                   new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(dist_id=2,
                   new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(dist_id=1,
                   new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.NO_NEW_CONSTRUCTION),
              dict(dist_id=1,
                   new_construct_year=constants.NO_NEW_CONSTRUCTION)]), 2)])
def test_get_schools_by_new_construction(description, test_input, expected,
                                         session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_by_new_construction() is according
    to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_schools_by_new_construction(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.TWO_THOUSAND_ONE)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.TWO_THOUSAND_ONE),
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND),
              dict(new_construct_year=constants.YEAR_TWO_THOUSAND)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1,
                   new_construct_year=constants.TWO_THOUSAND_ONE)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.TWO_THOUSAND_ONE),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.TWO_THOUSAND_ONE),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.YEAR_TWO_THOUSAND),
              dict(dist_id=2,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.YEAR_TWO_THOUSAND),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, new_construct_year=constants.YEAR_TWO_THOUSAND),
              dict(dist_id=1,
                   new_construct_year=constants.YEAR_TWO_THOUSAND)]), 2)])
def test_get_school_constructed_before_2000(description, test_input, expected,
                                            session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_constructed_before_2000() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_school_constructed_before_2000(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.TEN_SCHOOL_MEETING)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.TEN_SCHOOL_MEETING),
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.TEN_SCHOOL_MEETING)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.TEN_SCHOOL_MEETING),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.TEN_SCHOOL_MEETING),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(dist_id=2, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2)])
def test_get_school_with_no_school_meetings(description, test_input, expected,
                                            session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_with_no_school_meetings() is
    according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_school_with_no_school_meetings(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.HUNDRED)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.HUNDRED),
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.HUNDRED)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.HUNDRED),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.HUNDRED),
              dict(dist_id=1, sc_meetings=constants.TEN_SCHOOL_MEETING)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(dist_id=2, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_meetings=constants.TEN_SCHOOL_MEETING),
              dict(dist_id=1, sc_meetings=constants.NO_SCHOOL_MEETINGS)]), 2)])
def test_get_school_with_less_than_10_school_meetings(description, test_input,
                                                      expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_with_less_than_10_school_meetings()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_school_with_less_than_10_school_meetings(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_women=constants.HUNDRED)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_women=constants.HUNDRED),
              dict(sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_women=constants.NO_FEMALE_MEMBER),
              dict(sc_women=constants.NO_FEMALE_MEMBER)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_women=constants.HUNDRED)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_women=constants.HUNDRED),
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_women=constants.HUNDRED),
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER),
              dict(dist_id=2, sc_women=constants.NO_FEMALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER),
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER),
              dict(dist_id=1, sc_women=constants.NO_FEMALE_MEMBER)]), 2)])
def test_get_school_without_female_member_in_school_council(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_without_female_member_in_school_
    council() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_school_without_female_member_in_school_council(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(sc_men=constants.HUNDRED)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_men=constants.HUNDRED),
              dict(sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[
              dict(sc_men=constants.NO_MALE_MEMBER),
              dict(sc_men=constants.NO_MALE_MEMBER)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_men=constants.HUNDRED)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_men=constants.HUNDRED),
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_men=constants.HUNDRED),
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER),
              dict(dist_id=2, sc_men=constants.NO_MALE_MEMBER)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER),
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER),
              dict(dist_id=1, sc_men=constants.NO_MALE_MEMBER)]), 2)])
def test_get_school_without_male_member_in_school_council(
        description, test_input, expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_without_male_member_in_school
    _council() is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    session.commit()
    retrieved = models.School.get_school_without_male_member_in_school_council(
        test_input['dist_id'], test_input['count'])
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   classrooms=constants.HUNDRED)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.HUNDRED),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.HUNDRED)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.HUNDRED),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'is True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.HUNDRED),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, classrooms=constants.FOUR_CLASSROOMS),
              dict(emiscode=2, classrooms=constants.FOUR_CLASSROOMS)]), 2)])
def test_get_school_with_less_than_four_classrooms(description, test_input,
                                                   expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_with_less_than_four_classrooms()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_school_with_less_than_four_classrooms(
            test_input['dist_id'], test_input['count']))
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1,
                   openair_class=constants.HUNDRED)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.HUNDRED),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.HUNDRED)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.HUNDRED),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'is True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.HUNDRED),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, openair_class=constants.ONE_OPEN_AIR_CLASS),
              dict(emiscode=2, openair_class=constants.ONE_OPEN_AIR_CLASS)]), 2)])
def test_get_school_with_one_open_air_class(description, test_input,
                                             expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_with_one_open_air_class()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_school_with_one_open_air_class(
            test_input['dist_id'], test_input['count']))
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.HOCKEY)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[],
          sports_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.HOCKEY)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'is True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          sports_facilities_data=[
              dict(emiscode=1, hockey=constants.NO_HOCKEY),
              dict(emiscode=2, hockey=constants.NO_HOCKEY)]), 2)])
def test_get_schools_without_facilities_for_hockey(description, test_input,
                                             expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_schools_without_facilities_for_hockey()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['sports_facilities_data']:
        basic_facility = models.SportsFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_schools_without_facilities_for_hockey(
            test_input['dist_id'], test_input['count']))
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected


@pytest.mark.parametrize('description, test_input, expected', [
    ('In this test no data exist in database and district id is not given so '
     'method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is not given and one record exist in database '
     'but it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.TWO_THOUSAND_ONE)]), 0),
    ('In this test district id is not given and one record exist in database. '
     'The record fulfills the criteria so method should return 1 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is not given and two records exist in database '
     'but only one record fulfills the criteria so method should return 1 '
     'object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.TWO_THOUSAND_ONE),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is not given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=None, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 2),
    ('In this test district id is given but no data exist in database so '
     'method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[],
          academic_facilities_data=[]), 0),
    ('In this test district id is given and one record exist in database but '
     'it does not fulfills the criteria so method should return 0 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.TWO_THOUSAND_ONE)]), 0),
    ('In this test district id is given and one record exist in database. The '
     'record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.TWO_THOUSAND_ONE),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is given and two records exist in database but '
     'only one record fulfills the criteria so method should return 1 as count '
     'is True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.TWO_THOUSAND_ONE),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both record fulfills the criteria but one record district id is '
     'different than given district id so method should return 1 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=2)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 1),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 object.',
     dict(dist_id=1, count=False,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 2),
    ('In this test district id is given and two records exist in database. '
     'Both records fulfills the criteria so method should return 2 as count is '
     'True.',
     dict(dist_id=1, count=True,
          school_data=[dict(emiscode=1, dist_id=1),
                       dict(emiscode=2, dist_id=1)],
          academic_facilities_data=[
              dict(emiscode=1, total_books=constants.HUNDRED),
              dict(emiscode=2, total_books=constants.HUNDRED)]), 2)])
def test_get_school_with_less_than_hundred_books(description, test_input,
                                                 expected, session):
    """"In this test, we add record in School table according to test data and
    verify that output of method get_school_with_less_than_hundred_books()
    is according to test data.
    """
    for test_data in test_input['school_data']:
        school = models.School(**test_data)
        session.add(school)
    for test_data in test_input['academic_facilities_data']:
        basic_facility = models.AcademicFacilities(**test_data)
        session.add(basic_facility)
    session.commit()
    retrieved = (
        models.School.get_school_with_less_than_hundred_books(
            test_input['dist_id'], test_input['count']))
    if not test_input['count']:
        retrieved = len(retrieved)
    assert retrieved == expected

