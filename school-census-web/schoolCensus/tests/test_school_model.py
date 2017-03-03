"""Model School unit tests."""
import datetime as dt

import pytest

from schoolCensus.school_models.models import School

from .factories import UserFactory


@pytest.mark.usefixtures('session')
class TestSchoolModelMethodGetDistricts:
    """School model method get_districts tests."""

    def test_get_school_by_id(self):
        """Get school by by primary key i.e emiscode."""
        school = School(emiscode=12)
        school.save()

        retrieved = School.get_by_id(school.emiscode)
        assert retrieved == school
        assert retrieved.emiscode == school.emiscode
        assert retrieved.dist_id == school.dist_id

    def test_get_districts_with_no_record_in_db(self):
        """In this test no districts exist in database so get_districts method
        should return a empty list."""

        retrieved = School.get_districts()
        assert retrieved == []

    def test_get_districts_with_one_record_in_db(self):
        """In this test one district exist in database so get_districts method
        returns list containing one record."""

        first_school = School(dist_id=123, dist_nm='TestCity')
        first_school.save()
        retrieved = School.get_districts()
        assert len(retrieved) == 1
        assert retrieved[0].dist_id == first_school.dist_id
        assert retrieved[0].dist_nm == first_school.dist_nm

    def test_get_districts_with_with_dist_id(self):
        """In this test one district exist in database and get_districts method
        is called with this record district id."""

        first_school = School(dist_id=123, dist_nm='TestCity')
        first_school.save()
        retrieved = School.get_districts(first_school.dist_id)
        assert retrieved.dist_id == first_school.dist_id
        assert retrieved.dist_nm == first_school.dist_nm