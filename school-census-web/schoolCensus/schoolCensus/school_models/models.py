"""

"""
import math
from datetime import datetime

from sqlalchemy.sql import or_, and_
from schoolCensus import constants
from schoolCensus.database import Column, Model, db, relationship


class School(Model):
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
        query = cls.query.with_entities(cls.dist_id, cls.dist_nm).distinct()
        if dist_id:
            districts = query.filter(cls.dist_id == dist_id).first()
        else:
            districts = query.order_by(cls.dist_nm).all()
        return districts

    @classmethod
    def get_same_table_count(cls, criteria, district_id=None,
                             count_all=True):
        """"""
        operator = criteria['operator']

        query = cls.query
        if not count_all:
            if operator not in (constants.AND_OP, constants.OR_OP):
                field = criteria['field_name']
                value = criteria['value']
                query_field = getattr(cls, field)
                _filter = School.get_filter(query_field, value, operator)
            else:
                _filter = School.build_filter(
                    criteria[constants.OPERATOR_FIELDS], operator)
            query = query.filter(_filter)

        if district_id is not None:
            query = query.filter(cls.dist_id == district_id)
        if count_all and district_id is None:
            count = query.count()
        else:
            query = query.with_entities(db.func.count('*'))
            count = query.scalar()

        return count

    @classmethod
    def get_join_table_count(cls, criteria, district_id=None,
                             count_all=True):
        """"""
        operator = criteria['operator']
        field_model = criteria.get(constants.FIELD_MODEL_LABEL)

        join_model_class = globals()[field_model]
        query = cls.query.join(join_model_class)

        if not count_all:
            if operator not in (constants.AND_OP, constants.OR_OP):
                field = criteria['field_name']
                value = criteria['value']
                query_field = getattr(join_model_class, field)
                _filter = School.get_filter(query_field, value, operator)
            else:
                _filter = School.build_filter(
                    criteria[constants.OPERATOR_FIELDS], operator,
                    join_class=join_model_class)
            query = query.filter(_filter)

        if district_id is not None:
            query = query.filter(cls.dist_id == district_id)
        query = query.with_entities(db.func.count('*'))
        count = query.scalar()

        return count

    @classmethod
    def get_join_table_percentage_count(cls, criteria, district_id=None,
                                        count_all=True):
        """"""
        operator = criteria['operator']
        join_table = criteria[constants.FIELD_MODEL_LABEL]

        join_model_class = globals()[join_table]
        query = cls.query.join(join_model_class)

        if district_id is not None:
            query = query.filter(cls.dist_id == district_id)

        if not count_all:
            if operator not in (constants.AND_OP, constants.OR_OP):
                field = criteria['field_name']
                total_field = criteria['total_field_name']
                value = criteria['value']
                percentage_field = getattr(join_model_class, field)
                percentage_total_field = getattr(join_model_class, total_field)
                expression = (percentage_field / percentage_total_field) * 100
                _filter = School.get_filter(expression, value, operator)
            else:
                _filter = School.build_filter(
                    criteria[constants.OPERATOR_FIELDS], operator,
                    join_class=join_model_class)

            query = query.filter(_filter)

        query = query.with_entities(db.func.count('*'))
        count = query.scalar()

        return count

    @classmethod
    def district_schools_total_students(cls, dist_id):
        """"""
        query = cls.query.join(Enrollment)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            db.func.sum(Enrollment.total_no_of_students))
        total_students = query.all()[0][0]
        return total_students

    @classmethod
    def district_schools_total_teachers(cls, dist_id):
        """"""
        query = cls.query.join(TeachingStaff)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            db.func.sum(TeachingStaff.filled))
        total_teachers = query.all()[0][0]
        return total_teachers

    @classmethod
    def district_schools_students_teacher_ratio(cls, dist_id):
        """"""
        total_students = cls.district_schools_total_students(dist_id)
        total_students = float(total_students)
        total_teachers = cls.district_schools_total_teachers(dist_id)
        total_teachers = float(total_teachers)
        students_per_teacher_ratio = math.ceil(total_students/total_teachers)

        return students_per_teacher_ratio

    @classmethod
    def district_each_school_students_teacher_ratio(cls, dist_id):
        """

        :param dist_id: Integer district id
        :return: List of lists containing emiscode, students to teacher ratio
        """
        query = cls.query.join(Enrollment, TeachingStaff)
        query = query.filter(School.dist_id == dist_id)
        query = query.with_entities(
            School.emiscode,
            Enrollment.total_no_of_students/TeachingStaff.filled)
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
    def get_filter(cls, field, value, operator):
        """"""
        _filter = None
        assert value is not None, 'Given value must not be None'
        if operator == constants.EQUAL_OP:
            _filter = and_(field == value)
        elif operator == constants.IN_OP:
            assert isinstance(value, (list, tuple)), ('Given value must '
                                                      'not be None')
            _filter = and_(field.in_(value))
        elif operator == constants.NOT_OP:
            _filter = and_(field != value)
        elif operator == constants.LESS_THAN_OP:
            _filter = and_(field < value)
        elif operator == constants.LESS_THAN_EQUAL_TO_OP:
            _filter = and_(field <= value)
        elif operator == constants.GREATER_THAN_OP:
            _filter = and_(field > value)
        elif operator == constants.GREATER_THAN_EQUAL_OP:
            _filter = and_(field >= value)
        return _filter

    @classmethod
    def build_filter(cls, fields, operator, join_class=None):
        """"""
        _filter = []
        for field in fields:
            query_class = None
            if field['query_class'].lower() != 'cls':
                assert join_class is not None
                query_class = join_class
            field_name = field['field_name']
            field_operator = field['operator']
            field_value = field['value']
            query_field = getattr(query_class, field_name)
            field_filter = School.get_filter(query_field, field_value,
                                             field_operator)
            _filter.append(field_filter)
        if operator == constants.OR_OP:
            _filter = or_(*_filter)
        elif operator == constants.AND_OP:
            _filter = and_(*_filter)

        return _filter


class Enrollment(Model):
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
    __tablename__ = 'TeachingStaff'

    # id = Column(db.Integer, primary_key=True, autoincrement=True)
    emiscode = Column(db.Integer, db.ForeignKey('School.emiscode'), primary_key=True)
    sanctioned = Column(db.Integer)
    filled = Column(db.Integer)
    vacant = Column(db.Integer)


class AcademicFacilities(Model):
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
