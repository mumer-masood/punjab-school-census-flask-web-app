"""
This module contains the models classes for schoolCensus application.
"""
import math
from datetime import datetime

from sqlalchemy.sql import or_, and_, func
from schoolCensus import constants
from schoolCensus.database import Column, Model, db, relationship


class School(Model):
    """
    This table contains the school related data e.g emsicode as a primary key,
    area information, district information, contacts information etc.
    """
    __tablename__ = 'School'
    emiscode = Column(db.Integer, primary_key=True)
    school_name = Column(db.String(200))
    dist_id = Column(db.Integer)
    dist_nm = Column(db.String(150))
    teh_id = Column(db.Integer)
    teh_nm = Column(db.String(150))
    markazid = Column(db.String(50))
    markaznm = Column(db.String(150))
    muza = Column(db.String(150))
    address = Column(db.String(200))
    village_mohallah = Column(db.String(200))
    uc_name = Column(db.String(200))
    uc_no = Column(db.String(30))
    pp_no = Column(db.Integer)
    na_no = Column(db.Integer)
    head_name = Column(db.String(150))
    nidc_no = Column(db.String(30))
    head_charge = Column(db.Integer)
    head_grade = Column(db.Integer)
    resident_phone = Column(db.String(20))
    mobile_phone = Column(db.String(20))
    school_phone = Column(db.String(20))
    school_email = Column(db.String(150))
    contact_no = Column(db.String(20))
    school_status = Column(db.Integer)
    non_func_reason = Column(db.String(200))
    medium = Column(db.Integer)
    school_shift = Column(db.Integer)
    school_location = Column(db.Integer)
    gender_register = Column(db.Integer)
    school_gender = Column(db.String(20))
    gender_studying = Column(db.Integer)
    school_level = Column(db.String(50))
    consolidation_status = Column(db.Integer)
    school_type = Column(db.Integer)
    est_year = Column(db.Integer)
    upgrade_year_pri = Column(db.Integer)
    upgrade_year_mid = Column(db.Integer)
    upgrade_year_high = Column(db.Integer)
    upgrade_year_hsec = Column(db.Integer)
    bldg_status = Column(db.Integer)
    bldg_ownship = Column(db.Integer)
    place_status = Column(db.Integer)
    construct_type = Column(db.Integer)
    new_construct_year = Column(db.Integer)
    bldg_condition = Column(db.Integer)
    area_kanal = Column(db.Integer)
    area_marla = Column(db.Integer)
    covered_area = Column(db.Integer)
    uncover_kanal = Column(db.Integer)
    uncover_marla = Column(db.Integer)
    flood_affected = Column(db.String(100))
    flood_type = Column(db.String(150))
    po_bank_name = Column(db.String(200))
    sc_ac_no = Column(db.String(30))
    ac_open_date = Column(db.DateTime)
    ftf_collection = Column(db.String(50))
    govt_receive = Column(db.Integer)
    non_govt_receive = Column(db.Integer)
    amount_before = Column(db.Integer)
    amount_after = Column(db.Integer)
    expenses = Column(db.Integer)
    sc_meetings = Column(db.Integer)
    sc_total = Column(db.Integer)
    sc_women = Column(db.Integer)
    sc_men = Column(db.Integer)
    parent_member = Column(db.Integer)
    teacher_member = Column(db.Integer)
    general_member = Column(db.Integer)
    new_construct = Column(db.String(150))
    nsb_bank_name = Column(db.String(200))
    nsb_ac_no = Column(db.String(50))
    nsb_ac_date = Column(db.DateTime)
    nsb_before = Column(db.String(20))
    nsb_receive = Column(db.String(50))
    nsb_after = Column(db.String(50))
    nsb_expenditure = Column(db.String(50))
    dev_plan_date = Column(db.DateTime)
    doc = Column(db.DateTime, default=None)
    record_insert_date = Column(db.DateTime, default=datetime.utcnow)
    record_update_date = Column(db.DateTime)
    updated = Column(db.Boolean, default=0)
    update_tries = Column(db.Integer, default=0)

    academic_facilities = relationship('AcademicFacilities', uselist=False,
                                       backref='school')
    basic_facilities = relationship('BasicFacilities', backref='school',
                                    uselist=False)
    enrollment = relationship('Enrollment', backref='school',
                              uselist=False)
    sports_facilities = relationship('SportsFacilities', backref='school',
                                     uselist=False)
    teaching_staff = relationship('TeachingStaff', backref='school',
                                  uselist=False)

    @classmethod
    def get_districts(cls, dist_id=None):
        """
        Returns distinct district id and district name. If dist_id is provided then it limits
        the criteria, otherwise returns all.
        """
        query = cls.query.with_entities(cls.dist_id, cls.dist_nm).distinct()
        if dist_id:
            districts = query.filter(cls.dist_id == dist_id).first()
        else:
            districts = query.order_by(cls.dist_nm).all()
        return districts

    @classmethod
    def get_total_records(cls, dist_id=None):
        """
        This method return total number of schools and if dist_id is given then
        it return total number of schools in that district.

        :param dist_id: District id
        :return: Total number of records for given query
        """
        return (cls.query.filter_by(dist_id=dist_id).count() if dist_id else
                cls.query.count())

    @classmethod
    def get_join_table_total_records(cls, table_name, dist_id=None):
        """
        This method return total number of schools and if dist_id is given then
        it return total number of schools in that district.

        :param dist_id: District id
        :param table_name: Name of model
        :return: Total number of records for given query
        """
        join_model_class = globals()[table_name]
        query = cls.query.join(join_model_class)
        return (query.filter(cls.dist_id == dist_id).count() if dist_id else
                query.count())

    @classmethod
    def get_schools_by_new_construction(cls, dist_id=None, count=True):
        """
        This method returns the schools with no new construction after they were
        build i.e new_construct_year = 0 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (
            cls.query.filter(
                cls.new_construct_year == constants.NO_NEW_CONSTRUCTION,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter_by(
                new_construct_year=constants.NO_NEW_CONSTRUCTION))
        return query.count() if count else query.all()

    @classmethod
    def get_school_constructed_before_2000(cls, dist_id=None, count=True):
        """
        This method returns the schools with construction done before 2000 i.e
        new_construct_year less than equal to 2000 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (
            cls.query.filter(
                cls.new_construct_year <= constants.YEAR_TWO_THOUSAND,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter(
                cls.new_construct_year <= constants.YEAR_TWO_THOUSAND))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_no_school_meetings(cls, dist_id=None, count=True):
        """
        This method returns the schools which do not do school meetings i.e
        sc_meetings = 0 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (
            cls.query.filter(
                cls.sc_meetings == constants.NO_SCHOOL_MEETINGS,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter_by(
                sc_meetings=constants.NO_SCHOOL_MEETINGS))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_less_than_10_school_meetings(cls, dist_id=None,
                                                     count=True):
        """
        This method returns the schools which do less than 10 school meetings
        i.e sc_meetings less than 10 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (
            cls.query.filter(
                cls.sc_meetings <= constants.TEN_SCHOOL_MEETING,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter(
                cls.sc_meetings <= constants.TEN_SCHOOL_MEETING))
        return query.count() if count else query.all()

    @classmethod
    def get_school_without_female_member_in_school_council(cls, dist_id=None,
                                                           count=True):
        """
        This method returns the schools which do not have any female member in
        school council i.e sc_women = 0 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = (
            cls.query.filter(
                cls.sc_women == constants.NO_FEMALE_MEMBER,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter(
                cls.sc_women == constants.NO_FEMALE_MEMBER))
        return query.count() if count else query.all()

    @classmethod
    def get_school_without_male_member_in_school_council(cls, dist_id=None,
                                                         count=True):
        """
        This method returns the schools which do not have any male member in
        school council i.e sc_men = 0 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = (
            cls.query.filter(
                cls.sc_men == constants.NO_MALE_MEMBER,
                cls.dist_id == dist_id)
            if dist_id else cls.query.filter(
                cls.sc_men == constants.NO_MALE_MEMBER))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_less_than_four_classrooms(cls, dist_id=None, count=True):
        """
        This method returns schools which consist of less than 4 classrooms i.e
        classrooms <= 4 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.classrooms <= constants.FOUR_CLASSROOMS,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.classrooms <= constants.FOUR_CLASSROOMS))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_one_open_air_class(cls, dist_id=None, count=True):
        """
        This method returns schools which have one open air class i.e
        openair_class = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.openair_class == constants.ONE_OPEN_AIR_CLASS,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.openair_class == constants.ONE_OPEN_AIR_CLASS))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_without_facilities_for_hockey(cls, dist_id=None, count=True):
        """
        This method returns schools which have no facilities for hockey i.e
        hockey = 0 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(SportsFacilities)
        query = (query.filter(SportsFacilities.hockey == constants.NO_HOCKEY,
                              School.dist_id == dist_id) if dist_id else
                 query.filter(SportsFacilities.hockey == constants.NO_HOCKEY))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_less_than_hundred_books(cls, dist_id=None, count=True):
        """
        This method returns schools which contains less than 100 books in
        library i.e total_books <= 100 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.total_books <= constants.HUNDRED,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.total_books <= constants.HUNDRED))
        return query.count() if count else query.all()

    @classmethod
    def get_school_without_internet_access(cls, dist_id=None, count=True):
        """
        This method returns schools which do not have internet access i.e
        internet_evening = internet_morning = 0 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = query.filter(
            AcademicFacilities.internet_morning == constants.NO_INTERNET_ACCESS_MORNING,
            AcademicFacilities.internet_evening == constants.NO_INTERNET_ACCESS_EVENING)
        if dist_id:
            query = query.filter(School.dist_id == dist_id)
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_physics_lab_and_without_instrument(cls, dist_id=None,
                                                            count=True):
        """
        This method returns schools which have physics lab but does not have
        physics lab instrument i.e physics_lab = 1 and physics_instrument = 3
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.physics_lab == constants.PHYSICS_LAB,
            AcademicFacilities.physics_instrument == constants.NO_PHY_LAB_INS,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.physics_lab == constants.PHYSICS_LAB,
            AcademicFacilities.physics_instrument == constants.NO_PHY_LAB_INS))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_chemistry_lab_and_without_instrument(cls, dist_id=None,
                                                             count=True):
        """
        This method returns schools which have chemistry lab but does not have
        chemistry lab instrument i.e chemistry_lab = 1 and
        chemistry_instrument = 3 and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.chemistry_lab == constants.CHEMISTRY_LAB,
            AcademicFacilities.chemistry_instrument == constants.NO_CHE_LAB_INS,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.chemistry_lab == constants.CHEMISTRY_LAB,
            AcademicFacilities.chemistry_instrument == constants.NO_CHE_LAB_INS))

        return query.count() if count else query.all()

    @classmethod
    def get_school_with_biology_lab_and_without_instrument(cls, dist_id=None,
                                                           count=True):
        """
        This method returns schools which have biology lab but does not have
        biology lab instrument i.e biology_lab = 1 and biology_instrument = 3
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(
            AcademicFacilities.biology_lab == constants.BIOLOGY_LAB,
            AcademicFacilities.biology_instrument == constants.NO_BIO_LAB_INS,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            AcademicFacilities.biology_lab == constants.BIOLOGY_LAB,
            AcademicFacilities.biology_instrument == constants.NO_BIO_LAB_INS))
        return query.count() if count else query.all()

    @classmethod
    def get_school_with_less_than_fifty_percet_usable_toilets(cls, dist_id=None,
                                                              count=True):
        """
        This method returns schools which have less than 50% usable toilets i.e
        (toilet_usable/toilets_total)*100 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(BasicFacilities)
        query = (query.filter(
            ((BasicFacilities.toilet_usable / BasicFacilities.toilets_total) *
             constants.HUNDRED) <= constants.FIFTY,
            School.dist_id == dist_id)
                if dist_id else query.filter(
            ((BasicFacilities.toilet_usable / BasicFacilities.toilets_total) *
             constants.HUNDRED) <= constants.FIFTY))
        return query.count() if count else query.all()

    @classmethod
    def district_schools_total_students(cls, dist_id):
        """
        Get and return the count of total number of students in a given
        district's schools
        :param dist_id(int): District id
        :return(int): Count of total number of students in a given
        district's schools
        """
        query = cls.query.join(Enrollment)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            db.func.sum(Enrollment.total_no_of_students))
        total_students = query.all()[0][0]
        return total_students

    @classmethod
    def district_schools_total_teachers(cls, dist_id):
        """
        Get and return the count of total number of teachers in a given
        district's schools
        :param dist_id(int): District id
        :return(int): Count of total number of teachers in a given
        district's schools
        """
        query = cls.query.join(TeachingStaff)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            db.func.sum(TeachingStaff.filled))
        total_teachers = query.all()[0][0]
        return total_teachers

    @classmethod
    def district_schools_students_teacher_ratio(cls, dist_id):
        """
        Calculate and return the ratio of students per teacher in a given
        district's schools
        :param dist_id(int): District id
        :return(int): Ratio of students per teacher in a given
        district's schools
        """
        total_students = cls.district_schools_total_students(dist_id)
        total_students = float(total_students)
        total_teachers = cls.district_schools_total_teachers(dist_id)
        total_teachers = float(total_teachers)
        students_per_teacher_ratio = math.ceil(total_students/total_teachers)

        return students_per_teacher_ratio

    @classmethod
    def district_each_school_students_teacher_ratio(cls, dist_id):
        """
        Calculate and return the students to teacher ratio for each school
        in a given district.
        :param dist_id(int): District id
        :return(list): List of lists containing emiscode, students to teacher
        ratio
        """
        query = cls.query.join(Enrollment, TeachingStaff)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            School.emiscode,
            Enrollment.total_no_of_students/TeachingStaff.filled)
        query = query.order_by(School.emiscode)
        query_data = query.all()
        schools_data = []
        for index in xrange(len(query_data)):
            record = query_data[index]
            chart_index = index + 1
            try:
                school_data = [chart_index, math.ceil(record[1])]
            except Exception as e:
                print 'Error occured:%s Bad data found, data:%s' % (e,
                                                                    record[1])
                school_data = [chart_index, 0]
            schools_data.append(school_data)
        return schools_data

    @classmethod
    def get_schools_with_permanent_head_charge(cls, dist_id=None):
        """
        This method returns the schools with permanent head(principle) i.e
        head_charge = 1 and if dist_id is given then it returns schools of
        district with permanent head.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(cls.head_charge == constants.PERMANENT_HEAD_CHARGE,
                             cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                head_charge=constants.PERMANENT_HEAD_CHARGE).all())

    @classmethod
    def get_schools_with_additional_head_charge(cls, dist_id=None):
        """
        This method returns the schools with additional head(principle) i.e
        head_charge = 2 and if dist_id is given then it returns schools of
        district with permanent head.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(
                cls.head_charge == constants.ADDITIONAL_HEAD_CHARGE,
                cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                head_charge=constants.ADDITIONAL_HEAD_CHARGE).all())

    @classmethod
    def get_schools_with_lookafter_head_charge(cls, dist_id=None):
        """
        This method returns the schools with permanent head(principle) i.e
        head_charge = 3 and if dist_id is given then it returns schools of
        district with permanent head.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(
                cls.head_charge == constants.LOOKAFTER_HEAD_CHARGE,
                cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                head_charge=constants.LOOKAFTER_HEAD_CHARGE).all())

    @classmethod
    def get_functional_schools(cls, dist_id=None):
        """
        This method returns schools in functional state i.e school_status = 1
        and if dist_id is given then it returns functional schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(
                cls.school_status == constants.FUNCTIONAL_SCHOOLS,
                cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                school_status=constants.FUNCTIONAL_SCHOOLS).all())

    @classmethod
    def get_non_functional_schools(cls, dist_id=None, count=True):
        """
        This method returns schools in non functional state i.e
        school_status = 2 and if dist_id is given then it returns non functional
        schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (
            cls.query.filter(
                cls.school_status == constants.NON_FUNCTIONAL_SCHOOLS,
                cls.dist_id == dist_id) if dist_id else cls.query.filter(
                cls.school_status == constants.NON_FUNCTIONAL_SCHOOLS))
        return query.count() if count else query.all()

    @classmethod
    def get_merged_schools(cls, dist_id=None):
        """
        This method returns schools that are merged i.e school_status = 3
        and if dist_id is given then it returns merged schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_status == constants.MERGED_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_status=constants.MERGED_SCHOOLS).all())

    @classmethod
    def get_denotified_schools(cls, dist_id=None):
        """
        This method returns schools that are denotified. i.e school_status = 4
        and if dist_id is given then it returns denotified schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(cls.school_status == constants.DENOTIFIED_SCHOOLS,
                             cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                school_status=constants.DENOTIFIED_SCHOOLS).all())

    @classmethod
    def get_consolidated_schools(cls, dist_id=None):
        """
        This method returns schools that are consolidated. i.e school_status = 5
        and if dist_id is given then it returns consolidated schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_status == constants.CONSOLIDATED_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_status=constants.CONSOLIDATED_SCHOOLS).all())

    @classmethod
    def get_english_medium_schools(cls, dist_id=None):
        """
        This method returns english medium schools. i.e medium = 1 and if
        dist_id is given then it returns english medium schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.medium == constants.ENGLISH_MEDIUM,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            medium=constants.ENGLISH_MEDIUM).all())

    @classmethod
    def get_urdu_medium_schools(cls, dist_id=None, count=True):
        """
        This method returns urdu medium schools. i.e medium = 2 and if dist_id
        is given then it returns urdu medium schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(cls.medium == constants.URDU_MEDIUM,
                                  cls.dist_id == dist_id) if dist_id else
                 cls.query.filter_by(medium=constants.URDU_MEDIUM))
        return query.count() if count else query.all()

    @classmethod
    def get_both_urdu_and_english_medium_schools(cls, dist_id=None):
        """
        This method returns schools that teach in both urdu and english medium
        i.e medium = 3 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (
            cls.query.filter(cls.medium == constants.ENGLISH_AND_URDU_MEDIUM,
                             cls.dist_id == dist_id).all()
            if dist_id else cls.query.filter_by(
                medium=constants.ENGLISH_AND_URDU_MEDIUM).all())

    @classmethod
    def get_morning_shift_schools(cls, dist_id=None):
        """
        This method returns schools that are open in the morning i.e
        school_shift = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_shift == constants.MORNING_SHIFT,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_shift=constants.MORNING_SHIFT).all())

    @classmethod
    def get_evening_shift_schools(cls, dist_id=None):
        """
        This method returns schools that are open in the evening i.e
        school_shift = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_shift == constants.EVENING_SHIF,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_shift=constants.EVENING_SHIF).all())

    @classmethod
    def get_urban_schools(cls, dist_id=None):
        """
        This method returns schools that are open in the urban area i.e
        school_location = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_location == constants.URBAN_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_location=constants.URBAN_SCHOOLS).all())

    @classmethod
    def get_rural_schools(cls, dist_id=None):
        """
        This method returns schools that are open in the rural area i.e
        school_location = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_location == constants.RURAL_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_location=constants.RURAL_SCHOOLS).all())

    @classmethod
    def get_schools_closed_due_to_teachers_nonavailability(cls, dist_id=None,
                                                           count=True):
        """
        This method returns schools that are closed because there are no
        teachers i.e non_func_reason = 1 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.non_func_reason == constants.TEACHERS_NOT_AVAILABLE,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            non_func_reason=constants.TEACHERS_NOT_AVAILABLE))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_closed_due_to_students_nonavailability(cls, dist_id=None,
                                                           count=True):
        """
        This method returns schools that are closed because there are no
        students i.e non_func_reason = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.non_func_reason == constants.STUDENT_NOT_AVAILABLE,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            non_func_reason=constants.STUDENT_NOT_AVAILABLE))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_closed_due_to_building_nonavailability(cls, dist_id=None,
                                                           count=True):
        """
        This method returns schools that are closed because there is no
        building i.e non_func_reason = 3 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.non_func_reason == constants.BUILDING_NOT_AVAILABLE,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            non_func_reason=constants.BUILDING_NOT_AVAILABLE))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_closed_due_to_building_occupied(cls, dist_id=None,
                                                    count=True):
        """
        This method returns schools that are closed because building is occupied
        by someone else i.e non_func_reason = 4 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.non_func_reason == constants.BUILDING_OCCUPIED,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            non_func_reason=constants.BUILDING_OCCUPIED))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_only_for_boys(cls, dist_id=None):
        """
        This method returns schools that are only for boys i.e
        gender_register = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.gender_register == constants.BOYS_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            gender_register=constants.BOYS_SCHOOLS).all())

    @classmethod
    def get_schools_only_for_girls(cls, dist_id=None):
        """
        This method returns schools that are only for girls i.e
        gender_register = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.gender_register == constants.GIRLS_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            gender_register=constants.GIRLS_SCHOOLS).all())

    @classmethod
    def get_schools_only_boys_studying(cls, dist_id=None):
        """
        This method returns schools where only for boys are studying i.e
        gender_studying = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.gender_studying == constants.BOYS_STUDYING,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            gender_studying=constants.BOYS_STUDYING).all())

    @classmethod
    def get_schools_only_girls_studying(cls, dist_id=None):
        """
        This method returns schools where only for girls are studying i.e
        gender_studying = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.gender_studying == constants.GIRLS_STUDYING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            gender_studying=constants.GIRLS_STUDYING).all())

    @classmethod
    def get_schools_both_girl_and_boys_are_studying(cls, dist_id=None):
        """
        This method returns schools where both girls and boys are studying i.e
        gender_studying = 3 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.gender_studying == constants.GIRLS_AND_BOYS_STUDYING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            gender_studying=constants.GIRLS_AND_BOYS_STUDYING).all())

    @classmethod
    def get_mosque_schools(cls, dist_id=None):
        """
        This method returns schools with status equal to mosque schools i.e
        school_level = sMosque and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_level == constants.KEY_SMOSQUE,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_level=constants.KEY_SMOSQUE).all())

    @classmethod
    def get_primary_schools(cls, dist_id=None):
        """
        This method returns schools with status equal to primary i.e
        school_level = Primary and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_level == constants.KEY_PRIMARY,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_level=constants.KEY_PRIMARY).all())

    @classmethod
    def get_middle_schools(cls, dist_id=None):
        """
        This method returns schools with status equal to middle i.e
        school_level = middle and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_level == constants.KEY_MIDDLE,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_level=constants.KEY_MIDDLE).all())

    @classmethod
    def get_high_schools(cls, dist_id=None):
        """
        This method returns schools with status equal to high i.e
        school_level = High and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_level == constants.KEY_HIGH,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_level=constants.KEY_HIGH).all())

    @classmethod
    def get_higher_secondary_schools(cls, dist_id=None):
        """
        This method returns schools with status equal to higher secondary i.e
        school_level = H.Sec. and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_level == constants.KEY_HIGHER_SECONDARY,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_level=constants.KEY_HIGHER_SECONDARY).all())

    @classmethod
    def get_community_model_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to community model i.e
        school_type = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_type == constants.COMMUNITY_MODEL_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.COMMUNITY_MODEL_SCHOOLS).all())

    @classmethod
    def get_junior_model_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to junior model i.e
        school_type = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_type == constants.JUNIOR_MODEL_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.JUNIOR_MODEL_SCHOOLS).all())

    @classmethod
    def get_pilot_secondary_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to pilot_secondary i.e
        school_type = 3 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_type == constants.PILOT_SECONDARY_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.PILOT_SECONDARY_SCHOOLS).all())

    @classmethod
    def get_comprehensive_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to comprehensive i.e
        school_type = 4 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_type == constants.COMPREHENSIVE_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.COMPREHENSIVE_SCHOOLS).all())

    @classmethod
    def get_technical_high_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to technical high i.e
        school_type = 5 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_type == constants.TECH_HIGH_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.TECH_HIGH_SCHOOLS).all())

    @classmethod
    def get_model_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to model i.e school_type = 6
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.school_type == constants.MODEL_SCHOOLS,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.MODEL_SCHOOLS).all())

    @classmethod
    def get_local_government_schools(cls, dist_id=None):
        """
        This method returns schools with type equal to local government i.e
        school_type = 7 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.school_type == constants.LOCAL_GOVT_SCHOOLS,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            school_type=constants.LOCAL_GOVT_SCHOOLS).all())

    @classmethod
    def get_schools_with_building(cls, dist_id=None):
        """
        This method returns schools which are running in a building i.e
        bldg_status = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.bldg_status == constants.WITH_BUILDING,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_status=constants.WITH_BUILDING).all())

    @classmethod
    def get_schools_without_building(cls, dist_id=None):
        """
        This method returns schools which are running without a building i.e
        bldg_status = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.bldg_status == constants.WITHOUT_BUILDING,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_status=constants.WITHOUT_BUILDING).all())

    @classmethod
    def get_schools_with_building_owned_by_education_department(cls,
                                                                dist_id=None):
        """
        This method returns schools which have a building and it is owned by
        education department i.e bldg_ownship = 1 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.EDUCATION_DEPARTMENT_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.EDUCATION_DEPARTMENT_BUILDING).all())

    @classmethod
    def get_schools_with_building_owned_by_another_govt_school(cls,
                                                               dist_id=None):
        """
        This method returns schools which have a building and it is owned by
        another government department i.e bldg_ownship = 2 and if dist_id is
        given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.ANOTHER_SCHOOL_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.ANOTHER_SCHOOL_BUILDING).all())

    @classmethod
    def get_schools_with_building_is_on_lease(cls, dist_id=None):
        """
        This method returns schools which have a building but it is on lease
        i.e bldg_ownship = 3 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.ON_LEASE_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.ON_LEASE_BUILDING).all())

    @classmethod
    def get_schools_with_building_provided_by_local_population(cls, dist_id=None):
        """
        This method returns schools which have a building but it is provided by
        local population i.e bldg_ownship = 4 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.LOCAL_POPULATION_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.LOCAL_POPULATION_BUILDING).all())

    @classmethod
    def get_schools_with_building_is_owned_by_municipal_corporation(
            cls, dist_id=None):
        """
        This method returns schools which have a building but it is owned by
        municipal corporation i.e bldg_ownship = 5 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.MUNICIPAL_CORPORATION_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.MUNICIPAL_CORPORATION_BUILDING).all())

    @classmethod
    def get_schools_with_building_provided_by_school_council(cls, dist_id=None):
        """
        This method returns schools which have a building but it is provided by
        school_council i.e bldg_ownship = 6 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.SCHOOL_COUNCIL_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.SCHOOL_COUNCIL_BUILDING).all())

    @classmethod
    def get_schools_building_owned_by_other_govt_institute_than_municipal_corporation(
            cls, dist_id=None):
        """
        This method returns schools which have a building but it is owned by
        a government institution other then municipal corporation i.e
        bldg_ownship = 7 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_ownship == constants.NON_MUNICIPAL_CORPORATION_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.NON_MUNICIPAL_CORPORATION_BUILDING).all())

    @classmethod
    def get_schools_running_in_mosque(cls, dist_id=None):
        """
        This method returns schools which have a building but that building is
        mosque i.e bldg_ownship = 8 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.bldg_ownship == constants.MOSQUE_BUILDING,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_ownship=constants.MOSQUE_BUILDING).all())

    @classmethod
    def get_schools_running_in_a_place_where_government_created_them(
            cls, dist_id=None):
        """
        This method returns schools which are running in a location which was
        allocated by government i.e place_status = 1 and if dist_id is given
        then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.place_status == constants.GOVT_ALLOCATED_PLACE,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            place_status=constants.GOVT_ALLOCATED_PLACE).all())

    @classmethod
    def get_schools_not_running_in_a_place_where_government_created_them(
            cls, dist_id=None):
        """
        This method returns schools which are not running in a location which
        was allocated by government i.e place_status = 2 and if dist_id is given
        then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.place_status == constants.NOT_GOVT_ALLOCATED_PLACE,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            place_status=constants.NOT_GOVT_ALLOCATED_PLACE).all())

    @classmethod
    def get_schools_building_construction_type_is_mud(cls, dist_id=None):
        """
        This method returns schools which have a building made of mud i.e
        construct_type = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.construct_type == constants.MUD,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            construct_type=constants.MUD).all())

    @classmethod
    def get_schools_building_construction_type_is_concrete(cls, dist_id=None):
        """
        This method returns schools which have a building made of concrete i.e
        construct_type = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(cls.construct_type == constants.CONCRETE,
                                 cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            construct_type=constants.CONCRETE).all())

    @classmethod
    def get_schools_building_construction_type_is_both_concrete_and_mud(
            cls, dist_id=None):
        """
        This method returns schools which have a building which is made of both
        concrete and mud i.e construct_type = 3 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.construct_type == constants.MUD_AND_CONCRETE,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            construct_type=constants.MUD_AND_CONCRETE).all())

    @classmethod
    def get_schools_with_stable_building_condition(cls, dist_id=None):
        """
        This method returns schools which have a building and its condition is
        stable i.e bldg_condition = 1 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """

        return (cls.query.filter(
            cls.bldg_condition == constants.STABLE_BUILDING,
            cls.dist_id == dist_id).all()
                if dist_id else cls.query.filter_by(
            bldg_condition=constants.STABLE_BUILDING).all())

    @classmethod
    def get_schools_with_building_require_partial_renovation(cls, dist_id=None,
                                                             count=True):
        """
        This method returns schools which have a building and it requires some
        repairment i.e bldg_condition = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.bldg_condition == constants.SOME_REPAIRMENT,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            bldg_condition=constants.SOME_REPAIRMENT))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_building_require_full_renovation(cls, dist_id=None,
                                                          count=True):
        """
        This method returns schools which have a building but whole building
        requires repairment i.e bldg_condition = 3 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.bldg_condition == constants.FULL_REPAIRMENT,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            bldg_condition=constants.FULL_REPAIRMENT))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_building_condition_fully_dangerous(cls, dist_id=None,
                                                            count=True):
        """
        This method returns schools which have a building but building condition
        is fully dangerous i.e bldg_condition = 4 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.bldg_condition == constants.FULLY_DANGEROUS_BUILDING,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            bldg_condition=constants.FULLY_DANGEROUS_BUILDING))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_building_condition_partially_dangerous(
            cls, dist_id=None, count=True):
        """
        This method returns schools which have a building but building condation
        is partially dangerous i.e bldg_condition = 5 and if dist_id is given
        then it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """

        query = (cls.query.filter(
            cls.bldg_condition == constants.PARTIALLY_DANGEROUS_BUILDING,
            cls.dist_id == dist_id)
                if dist_id else cls.query.filter_by(
            bldg_condition=constants.PARTIALLY_DANGEROUS_BUILDING))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_drinking_water_facilities_available(cls, dist_id=None):
        """
        This method returns schools which have facilities for drinking water and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water == constants.DRINKING_WATER_AVAILABLE,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water ==
            constants.DRINKING_WATER_AVAILABLE).all())

    @classmethod
    def get_schools_without_drinking_water_facilities(cls, dist_id=None):
        """
        This method returns schools which do not have facilities for drinking
        water and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water == constants.DRINKING_WATER_NOT_AVAILABLE,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water ==
            constants.DRINKING_WATER_NOT_AVAILABLE).all())

    @classmethod
    def get_schools_with_drinking_water_facilities_not_working(cls, dist_id=None):
        """
        This method returns schools which have facilities for drinking
        water but they are not in working condition and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water == constants.DRINKING_WATER_NOT_WORKING,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water ==
            constants.DRINKING_WATER_NOT_WORKING).all())

    @classmethod
    def get_schools_with_drinking_water_source_is_well(cls, dist_id=None):
        """
        This method returns schools where drinking water source is well i.e
        drink_water_type = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(BasicFacilities.drink_water_type == constants.WELL,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.drink_water_type == constants.WELL).all())

    @classmethod
    def get_schools_where_drinking_water_source_is_hand_pump(cls, dist_id=None):
        """
        This method returns schools where drinking water source is hand pump i.e
        drink_water_type = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water_type == constants.HAND_PUMP,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water_type == constants.HAND_PUMP).all())

    @classmethod
    def get_schools_where_drinking_water_source_is_water_pump(cls, dist_id=None):
        """
        This method returns schools where drinking water source is water pump
        i.e drink_water_type = 3 and if dist_id is given then it returns schools
        of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water_type == constants.WATER_PUMP,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water_type == constants.WATER_PUMP).all())

    @classmethod
    def get_schools_where_drinking_water_source_is_govt_null(cls, dist_id=None):
        """
        This method returns schools where drinking water source is government
        null i.e drink_water_type = 4 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water_type == constants.GOVT_NULL,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water_type == constants.GOVT_NULL).all())

    @classmethod
    def get_schools_where_drinking_water_source_is_other(cls, dist_id=None):
        """
        This method returns schools where drinking water source is other than
        well, hand pump, water pump and government null i.e drink_water_type = 5
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.drink_water_type == constants.OTHER_WATER_TYPE,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.drink_water_type ==
            constants.OTHER_WATER_TYPE).all())

    @classmethod
    def get_schools_with_electricity(cls, dist_id=None):
        """
        This method returns schools which have electricity i.e electricity = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity == constants.WITH_ELECTRICITY,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity == constants.WITH_ELECTRICITY).all())

    @classmethod
    def get_schools_with_no_electricity(cls, dist_id=None):
        """
        This method returns schools which have no electricity i.e
        electricity = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity == constants.WITHOUT_ELECTRICITY,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity == constants.WITHOUT_ELECTRICITY).all())

    @classmethod
    def get_schools_with_electricity_not_working(cls, dist_id=None):
        """
        This method returns schools which have electricity but not in working
        condition i.e electricity = 3 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity == constants.ELECTRICITY_NOT_WORKING,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity == constants.ELECTRICITY_NOT_WORKING).all())

    @classmethod
    def get_schools_without_electricity_due_to_bill_not_paid(cls, dist_id=None):
        """
        This method returns schools which have no electricity and the reason is
        electricity bill not paid i.e electricity_reasons = 1 and if dist_id is
        given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity_reasons == constants.UNPAID_BILL,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity_reasons == constants.UNPAID_BILL).all())

    @classmethod
    def get_schools_with_no_electricity_due_to_faulty_wiring(cls, dist_id=None):
        """
        This method returns schools which have no electricity and its reason is
        faulty waring i.e electricity_reasons = 2 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity_reasons == constants.FAULTY_WIRING,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity_reasons == constants.FAULTY_WIRING).all())

    @classmethod
    def get_schools_with_no_electricity_due_to_no_connection(cls, dist_id=None):
        """
        This method returns schools which have no electricity because of no
        electricity connection i.e electricity_reasons = 3 and if dist_id is
        given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.electricity_reasons == constants.NO_CONNECTION,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.electricity_reasons == constants.NO_CONNECTION).all())

    @classmethod
    def get_schools_with_toilets(cls, dist_id=None):
        """
        This method returns schools which have toilets i.e toilets = 1 and if
        dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(BasicFacilities.toilets == constants.WITH_TOILETS,
                             School.dist_id == dist_id).all() if dist_id else
                query.filter(
                    BasicFacilities.toilets == constants.WITH_TOILETS).all())

    @classmethod
    def get_schools_with_no_toilets(cls, dist_id=None):
        """
        This method returns schools which have no toilets i.e toilets = 2 and if
        dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.toilets == constants.WITHOUT_TOILETS,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.toilets == constants.WITHOUT_TOILETS).all())

    @classmethod
    def get_schools_with_nonfunctional_toilets(cls, dist_id=None):
        """
        This method returns schools which have toilets but they are not
        functional condition i.e toilets = 3 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.toilets == constants.NONFUNCTIONAL_TOILETS,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.toilets == constants.NONFUNCTIONAL_TOILETS).all())

    @classmethod
    def get_schools_with_boundary_wall(cls, dist_id=None):
        """
        This method returns schools which have boundary wall i.e
        boundary_wall = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.boundary_wall == constants.BOUNDARY_WALL,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.boundary_wall == constants.BOUNDARY_WALL).all())

    @classmethod
    def get_schools_without_boundary_wall(cls, dist_id=None):
        """
        This method returns schools which have no boundary wall i.e
        boundary_wall = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.boundary_wall == constants.WITHOUT_BOUNDARY_WALL,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.boundary_wall ==
            constants.WITHOUT_BOUNDARY_WALL).all())

    @classmethod
    def get_schools_with_complete_boundary_wall(cls, dist_id=None):
        """
        This method returns schools which have complete boundary wall i.e
        bwall_complete = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.bwall_complete == constants.COMPLETE_BOUNDARY_WALL,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.bwall_complete == constants.COMPLETE_BOUNDARY_WALL).all())

    @classmethod
    def get_schools_with_incomplete_boundary_wall(cls, dist_id=None):
        """
        This method returns schools which have incomplete boundary wall i.e
        bwall_complete = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.bwall_complete == constants.INCOMPLETE_BOUNDARY_WALL,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.bwall_complete == constants.INCOMPLETE_BOUNDARY_WALL).all())

    @classmethod
    def get_schools_with_boundary_wall_in_bad_condition(cls, dist_id=None):
        """
        This method returns schools which have boundary wall but its condition
        is bad i.e bwall_complete = 3 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.bwall_complete == constants.BAD_BOUNDARY_WALL,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            BasicFacilities.bwall_complete == constants.BAD_BOUNDARY_WALL).all())

    @classmethod
    def get_schools_with_main_gate(cls, dist_id=None):
        """
        This method returns schools which have main gate i.e main_gate = 1 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(BasicFacilities.main_gate == constants.MAIN_GATE,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.main_gate == constants.MAIN_GATE).all())

    @classmethod
    def get_schools_without_main_gate(cls, dist_id=None):
        """
        This method returns schools which have main gate i.e main_gate = 2 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.main_gate == constants.WITHOUT_MAIN_GATE,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.main_gate == constants.WITHOUT_MAIN_GATE).all())

    @classmethod
    def get_schools_with_sewerage_system(cls, dist_id=None):
        """
        This method returns schools which have sewerage system i.e sewerage = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.sewerage == constants.SEWERAGE_SYSTEM,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.sewerage == constants.SEWERAGE_SYSTEM).all())

    @classmethod
    def get_schools_without_sewerage_system(cls, dist_id=None):
        """
        This method returns schools which have sewerage system i.e sewerage = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(BasicFacilities)
        return (query.filter(
            BasicFacilities.sewerage == constants.NO_SEWERAGE_SYSTEM,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            BasicFacilities.sewerage == constants.NO_SEWERAGE_SYSTEM).all())

    @classmethod
    def get_schools_with_playground(cls, dist_id=None):
        """
        This method returns schools which have playground i.e play_ground = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(
            SportsFacilities.play_ground == constants.PLAYGROUND,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.play_ground == constants.PLAYGROUND).all())

    @classmethod
    def get_schools_without_playground(cls, dist_id=None):
        """
        This method returns schools which have playground i.e play_ground = 2
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(
            SportsFacilities.play_ground == constants.NO_PLAYGROUND,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.play_ground == constants.NO_PLAYGROUND).all())

    @classmethod
    def get_schools_with_facilities_for_cricket(cls, dist_id=None):
        """
        This method returns schools which have facilities for cricket i.e
        cricket = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(SportsFacilities.circket == constants.CRICKET,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.circket == constants.CRICKET).all())

    @classmethod
    def get_schools_with_facilities_for_football(cls, dist_id=None):
        """
        This method returns schools which have facilities for football i.e
        football = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(SportsFacilities.football == constants.FOOTBALL,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.football == constants.FOOTBALL).all())

    @classmethod
    def get_schools_with_facilities_for_hockey(cls, dist_id=None):
        """
        This method returns schools which have facilities for hockey i.e
        hockey = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(SportsFacilities.hockey == constants.HOCKEY,
                             School.dist_id == dist_id).all()
                if dist_id else
                query.filter(SportsFacilities.hockey == constants.HOCKEY).all())

    @classmethod
    def get_schools_with_facilities_for_badminton(cls, dist_id=None):
        """
        This method returns schools which have facilities for badminton i.e
        football = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(SportsFacilities.badminton == constants.BADMINTON,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.badminton == constants.BADMINTON).all())

    @classmethod
    def get_schools_with_facilities_for_volleyball(cls, dist_id=None):
        """
        This method returns schools which have facilities for badminton i.e
        volleyball = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(
            SportsFacilities.volleyball == constants.VOLLEY_BALL,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.volleyball == constants.VOLLEY_BALL).all())

    @classmethod
    def get_schools_with_facilities_for_table_tennis(cls, dist_id=None):
        """
        This method returns schools which have facilities for table tennis i.e
        table_tennis = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(
            SportsFacilities.table_tennis == constants.TABLE_TENNIS,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.table_tennis == constants.TABLE_TENNIS).all())

    @classmethod
    def get_schools_with_facilities_for_other_sports(cls, dist_id=None):
        """
        This method returns schools which have facilities for sports other than
        cricket, football, hockey, badminton, volleyball and table tennis i.e
        other = 1 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(SportsFacilities)
        return (query.filter(SportsFacilities.other == constants.OTHER_SPORTS,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            SportsFacilities.other == constants.OTHER_SPORTS).all())

    @classmethod
    def get_schools_with_library(cls, dist_id=None):
        """
        This method returns schools which have library i.e library = 1 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.library == constants.LIBRARY,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.library == constants.LIBRARY).all())

    @classmethod
    def get_schools_without_library(cls, dist_id=None):
        """
        This method returns schools which have no library i.e library = 2 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.library == constants.NO_LIBRARY,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.library == constants.NO_LIBRARY).all())

    @classmethod
    def get_schools_with_lab(cls, dist_id=None):
        """
        This method returns schools which have lab i.e lab_exist = 1 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.lab_exist == constants.LAB,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.lab_exist == constants.LAB).all())

    @classmethod
    def get_schools_without_lab(cls, dist_id=None, count=True):
        """
        This method returns schools which have no lab i.e lab_exist = 2 and
        if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :param count: This flag is used to get the count of total number of
        records for given query
        :return: Total number of records for given query or List of School model
        instances
        """
        query = cls.query.join(AcademicFacilities)
        query = (query.filter(AcademicFacilities.lab_exist == constants.NO_LAB,
                              School.dist_id == dist_id) if dist_id else
                 query.filter(AcademicFacilities.lab_exist == constants.NO_LAB))
        return query.count() if count else query.all()

    @classmethod
    def get_schools_with_physics_lab(cls, dist_id=None):
        """
        This method returns schools which have physics lab i.e physics_lab = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.physics_lab == constants.PHYSICS_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.physics_lab == constants.PHYSICS_LAB).all())

    @classmethod
    def get_schools_without_physics_lab(cls, dist_id=None):
        """
        This method returns schools which have no physics lab i.e
        physics_lab = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.physics_lab == constants.NO_PHYSICS_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.physics_lab == constants.NO_PHYSICS_LAB).all())

    @classmethod
    def get_schools_with_biology_lab(cls, dist_id=None):
        """
        This method returns schools which have biology lab i.e biology_lab = 1
        and if dist_id is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.biology_lab == constants.BIOLOGY_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.biology_lab == constants.BIOLOGY_LAB).all())

    @classmethod
    def get_schools_without_biology_lab(cls, dist_id=None):
        """
        This method returns schools which have no biology lab i.e
        biology_lab = 2 and if dist_id is given then it returns schools of that
        district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.biology_lab == constants.NO_BIOLOGY_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.biology_lab == constants.NO_BIOLOGY_LAB).all())

    @classmethod
    def get_schools_with_chemistry_lab(cls, dist_id=None):
        """
        This method returns schools which have chemistry lab i.e
        chemistry_lab = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.chemistry_lab == constants.CHEMISTRY_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.chemistry_lab == constants.CHEMISTRY_LAB).all())

    @classmethod
    def get_schools_without_chemistry_lab(cls, dist_id=None):
        """
        This method returns schools which have no chemistry lab i.e
        chemistry_lab = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.chemistry_lab == constants.NO_CHEMISTRY_LAB,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            AcademicFacilities.chemistry_lab == constants.NO_CHEMISTRY_LAB).all())

    @classmethod
    def get_schools_with_home_economics_lab(cls, dist_id=None):
        """
        This method returns schools which have homo economics lab i.e
        homeconomics_lab = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.homeconomics_lab == constants.HOME_ECONOMICS_LAB,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            AcademicFacilities.homeconomics_lab ==
            constants.HOME_ECONOMICS_LAB).all())

    @classmethod
    def get_schools_without_home_economics_lab(cls, dist_id=None):
        """
        This method returns schools which have no homo economics lab i.e
        homeconomics_lab = 2 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.homeconomics_lab ==
                             constants.NO_HOME_ECONOMICS_LAB,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.homeconomics_lab ==
            constants.NO_HOME_ECONOMICS_LAB).all())

    @classmethod
    def get_schools_with_combine_lab_for_science_subjects(cls, dist_id=None):
        """
        This method returns schools which have combine lab for science subjects
        i.e combine_lab = 1 and if dist_id is given then it returns schools of
        that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.combine_lab == constants.COMBINE_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.combine_lab == constants.COMBINE_LAB).all())

    @classmethod
    def get_schools_without_combine_lab_for_science_subjects(cls, dist_id=None):
        """
        This method returns schools which do not have combine lab for science
        subjects i.e combine_lab = 2 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.combine_lab == constants.NO_COMBINE_LAB,
            School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.combine_lab == constants.NO_COMBINE_LAB).all())

    @classmethod
    def get_schools_with_enough_instrument_for_physics_lab(cls, dist_id=None):
        """
        This method returns schools which have enough instrument for physics lab
        i.e physics_instrument = 1 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.physics_instrument ==
            constants.PHYSICS_LAB_INSTRUMENT, School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.physics_instrument ==
            constants.PHYSICS_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_without_enough_instrument_for_physics_lab(cls, dist_id=None):
        """This method returns schools which do not have enough instrument for
        i.e physics lab physics_instrument = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.physics_instrument ==
                             constants.NO_PHYSICS_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.physics_instrument ==
            constants.NO_PHYSICS_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_with_enough_instrument_for_biology_lab(cls, dist_id=None):
        """
        This method returns schools which have enough instrument for biology lab
        i.e biology_instrument = 1 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.biology_instrument ==
                             constants.BIOLOGY_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.biology_instrument ==
            constants.BIOLOGY_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_without_enough_instrument_for_biology_lab(cls, dist_id=None):
        """
        This method returns schools which do not have enough instrument for
        biology lab i.e biology_instrument = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.biology_instrument ==
                             constants.NO_BIOLOGY_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.biology_instrument ==
            constants.NO_BIOLOGY_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_with_enough_instrument_for_chemistry_lab(cls, dist_id=None):
        """
        This method returns schools which have enough instrument for chemistry
        lab i.e chemistry_instrument = 1 and if dist_id is given then it returns
        schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.chemistry_instrument ==
                             constants.CHEMISTRY_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.chemistry_instrument ==
            constants.CHEMISTRY_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_without_enough_instrument_for_chemistry_lab(cls,
                                                                dist_id=None):
        """
        This method returns schools which do not have enough instrument for
        chemistry lab i.e chemistry_instrument = 2 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.chemistry_instrument ==
                             constants.NO_CHEMISTRY_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.chemistry_instrument ==
            constants.NO_CHEMISTRY_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_with_enough_instrument_for_home_economics_lab(cls,
                                                                  dist_id=None):
        """
        This method returns schools which have enough instrument for home
        economics lab i.e home_instrument = 1 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.home_instrument ==
                             constants.HOME_ECONOMICS_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.home_instrument ==
            constants.HOME_ECONOMICS_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_without_enough_instrument_for_home_economics_lab(
            cls, dist_id=None):
        """
        This method returns schools which do not have enough instrument for home
        economics lab i.e home_instrument = 2 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.home_instrument ==
                             constants.NO_HOME_ECONOMICS_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.home_instrument ==
            constants.NO_HOME_ECONOMICS_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_with_enough_instrument_for_combine_lab(cls, dist_id=None):
        """
        This method returns schools which have enough instrument for combine lab
        science subjects i.e combine_instrument = 1 and if dist_id is given then
        it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.combine_instrument ==
                             constants.COMBINE_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.combine_instrument ==
            constants.COMBINE_LAB_INSTRUMENT).all())

    @classmethod
    def get_schools_without_enough_instrument_for_combine_lab(cls,
                                                              dist_id=None):
        """
        This method returns schools which do not have enough instrument for
        combine lab science subjects i.e combine_instrument = 2 and if dist_id
        is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.combine_instrument ==
                             constants.NO_COMBINE_LAB_INSTRUMENT,
                             School.dist_id == dist_id).all()
                if dist_id else
                query.filter(AcademicFacilities.combine_instrument ==
                             constants.NO_COMBINE_LAB_INSTRUMENT).all())

    @classmethod
    def get_morning_shift_schools_with_computer_lab(cls, dist_id=None):
        """
        This method returns schools which are open in morning session and have
        computer lab i.e com_lab_morning = 1 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.com_lab_morning ==
                             constants.MORNING_COMPUTER_LAB,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.com_lab_morning ==
            constants.MORNING_COMPUTER_LAB).all())

    @classmethod
    def get_morning_shift_schools_without_computer_lab(cls, dist_id=None):
        """
        This method returns schools which are open in morning and do not have
        computer lab i.e com_lab_morning = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.com_lab_morning ==
                             constants.NO_MORNING_COMPUTER_LAB,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.com_lab_morning ==
            constants.NO_MORNING_COMPUTER_LAB).all())

    @classmethod
    def get_evening_shift_schools_with_computer_lab(cls, dist_id=None):
        """
        This method returns schools which are open in evening session and have
        computer lab i.e com_lab_evening = 1 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(
            AcademicFacilities.com_lab_evening == constants.EVENING_COMPUTER_LAB,
            School.dist_id == dist_id).all() if dist_id else query.filter(
            AcademicFacilities.com_lab_evening ==
            constants.EVENING_COMPUTER_LAB).all())

    @classmethod
    def get_evening_shift_schools_without_computer_lab(cls, dist_id=None):
        """
        This method returns schools which are open in evening and do not have
        computer lab i.e com_lab_evening = 2 and if dist_id is given then it
        returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.com_lab_evening ==
                             constants.NO_EVENING_COMPUTER_LAB,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.com_lab_evening ==
            constants.NO_EVENING_COMPUTER_LAB).all())

    @classmethod
    def get_morning_shift_schools_with_internet_in_computer_lab(
            cls, dist_id=None):
        """
        This method returns schools which are open in morning and have internet
        access in computer lab i.e internet_morning = 1 and if dist_id is given
        then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.internet_morning ==
                             constants.INTERNET_ACCESS_MORNING,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.internet_morning ==
            constants.INTERNET_ACCESS_MORNING).all())

    @classmethod
    def get_morning_shift_schools_without_internet_in_computer_lab(
            cls, dist_id=None):
        """
        This method returns schools which are open in morning and do not have
        internet access in computer lab i.e internet_morning = 2 and if dist_id
        is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.internet_morning ==
                             constants.NO_INTERNET_ACCESS_MORNING,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.internet_morning ==
            constants.NO_INTERNET_ACCESS_MORNING).all())

    @classmethod
    def get_evening_shift_schools_with_internet_in_computer_lab(
            cls, dist_id=None):
        """
        This method returns schools which are open in evening and have internet
        access in computer lab i.e internet_evening = 1 and if dist_id is given
        then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.internet_evening ==
                             constants.INTERNET_ACCESS_EVENING,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.internet_evening ==
            constants.INTERNET_ACCESS_EVENING).all())

    @classmethod
    def get_evening_shift_schools_without_internet_in_computer_lab(
            cls, dist_id=None):
        """
        This method returns schools which are open in evening and do not have
        internet access in computer lab i.e internet_evening = 2 and if dist_id
        is given then it returns schools of that district.

        :param dist_id: District id
        :return: List of School model instances
        """
        query = cls.query.join(AcademicFacilities)
        return (query.filter(AcademicFacilities.internet_evening ==
                             constants.NO_INTERNET_ACCESS_EVENING,
                             School.dist_id == dist_id).all()
                if dist_id else query.filter(
            AcademicFacilities.internet_evening ==
            constants.NO_INTERNET_ACCESS_EVENING).all())


class Enrollment(Model):
    """
    This table contains the all classes fields but only total number of students field contains data.
    Fyi, total no of students data is scraped from Punjab schools portal site.
    """
    __tablename__ = 'Enrollment'

    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    eng_kachi_b = Column(db.Integer)
    eng_kachi_g = Column(db.Integer)
    eng_cls1_b = Column(db.Integer)
    eng_cls1_g = Column(db.Integer)
    eng_cls2_b = Column(db.Integer)
    eng_cls2_g = Column(db.Integer)
    eng_cls3_b = Column(db.Integer)
    eng_cls3_g = Column(db.Integer)
    eng_cls4_b = Column(db.Integer)
    eng_cls4_g = Column(db.Integer)
    eng_cls5_b = Column(db.Integer)
    eng_cls5_g = Column(db.Integer)
    eng_cls6_b = Column(db.Integer)
    eng_cls6_g = Column(db.Integer)
    eng_cls7_b = Column(db.Integer)
    eng_cls7_g = Column(db.Integer)
    eng_cls8_b = Column(db.Integer)
    eng_cls8_g = Column(db.Integer)
    eng_cls9_b = Column(db.Integer)
    eng_cls9_g = Column(db.Integer)
    eng_cls10_b = Column(db.Integer)
    eng_cls10_g = Column(db.Integer)
    cs_cls9 = Column(db.Integer)
    cs_cls10 = Column(db.Integer)
    bio_cls9 = Column(db.Integer)
    bio_cls10 = Column(db.Integer)
    ee_kachi = Column(db.Integer)
    ee_cls1 = Column(db.Integer)
    ee_cls2 = Column(db.Integer)
    ee_cls3 = Column(db.Integer)
    ee_cls4 = Column(db.Integer)
    ee_cls5 = Column(db.Integer)
    ee_other = Column(db.Integer)
    total_no_of_students = Column(db.Integer, default=0)


class TeachingStaff(Model):
    """
    This table contains the information for teaching staff in schools e.g. total no of sanctioned seats, total no of filled seats etc.
    """
    __tablename__ = 'TeachingStaff'

    # id = Column(db.Integer, primary_key=True, autoincrement=True)
    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    sanctioned = Column(db.Integer)
    filled = Column(db.Integer)
    vacant = Column(db.Integer)


class AcademicFacilities(Model):
    """
    This table contains the information for academic facilities e.g. library, laboratory etc information.
    """
    __tablename__ = 'AcademicFacilities'

    # id = Column(db.Integer, primary_key=True, autoincrement=True)
    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    teacher_nofurniture = Column(db.Integer, default=None)
    student_nofurniture = Column(db.Integer, default=None)
    library = Column(db.Integer, default=None)
    if_yes = Column(db.Integer, default=None)
    total_books = Column(db.Integer, default=None)
    lab_exist = Column(db.Integer, default=None)
    physics_lab = Column(db.Integer, default=None)
    biology_lab = Column(db.Integer, default=None)
    chemistry_lab = Column(db.Integer, default=None)
    homeconomics_lab = Column(db.Integer, default=None)
    combine_lab = Column(db.Integer, default=None)
    physics_instrument = Column(db.Integer, default=None)
    biology_instrument = Column(db.Integer, default=None)
    chemistry_instrument = Column(db.Integer, default=None)
    home_instrument = Column(db.Integer, default=None)
    combine_instrument = Column(db.Integer, default=None)
    com_lab_morning = Column(db.Integer, default=None)
    com_no_morning = Column(db.Integer, default=None)
    student_morning = Column(db.Integer, default=None)
    com_lab_evening = Column(db.Integer, default=None)
    com_no_evening = Column(db.Integer, default=None)
    student_evening = Column(db.Integer, default=None)
    internet_morning = Column(db.Integer, default=None)
    internet_evening = Column(db.Integer, default=None)
    classrooms = Column(db.Integer, default=None)
    classes = Column(db.Integer, default=None)
    sections = Column(db.Integer, default=None)
    openair_class = Column(db.Integer, default=None)


class BasicFacilities(Model):
    """
    This table contains the information for basic facilities in schools e.g. drinking water,
    toilets, boundary walls etc.
    """
    __tablename__ = 'BasicFacilities'
    # id = Column(db.Integer, primary_key=True, autoincrement=True)
    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    drink_water = Column(db.Integer, default=None)
    drink_water_type = Column(db.Integer, default=None)
    electricity = Column(db.Integer, default=None)
    electricity_reasons = Column(db.Integer, default=None)
    toilets = Column(db.Integer, default=None)
    toilets_total = Column(db.Integer, default=None)
    toilet_usable = Column(db.Integer, default=None)
    toilet_needrepair = Column(db.Integer, default=None)
    toilet_teachers = Column(db.Integer, default=None)
    boundary_wall = Column(db.Integer, default=None)
    bwall_complete = Column(db.Integer, default=None)
    main_gate = Column(db.Integer, default=None)
    sewerage = Column(db.Integer, default=None)


class SportsFacilities(Model):
    """
    This table contains the information for sports facilities in a school etc.
    """
    __tablename__ = 'SportsFacilities'

    # id = Column(db.Integer, primary_key=True, autoincrement=True)
    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    play_ground = Column(db.Integer, default=None)
    circket = Column(db.Integer, default=None)
    football = Column(db.Integer, default=None)
    hockey = Column(db.Integer, default=None)
    badminton = Column(db.Integer, default=None)
    volleyball = Column(db.Integer, default=None)
    table_tennis = Column(db.Integer, default=None)
    other = Column(db.Integer, default=None)
