"""

"""
from sqlalchemy import (Column, Integer, ForeignKey)

from base_model import QueryMixin


class AcademicFacilities(QueryMixin):
    __tablename__ = 'AcademicFacilities'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    emiscode = Column(Integer, ForeignKey('School.emiscode'), primary_key=True)
    teacher_nofurniture = Column(Integer, default=None)
    student_nofurniture = Column(Integer, default=None)
    library = Column(Integer, default=None)
    if_yes = Column(Integer, default=None)
    total_books = Column(Integer, default=None)
    lab_exist = Column(Integer, default=None)
    physics_lab = Column(Integer, default=None)
    biology_lab = Column(Integer, default=None)
    chemistry_lab = Column(Integer, default=None)
    homeconomics_lab = Column(Integer, default=None)
    combine_lab = Column(Integer, default=None)
    physics_instrument = Column(Integer, default=None)
    biology_instrument = Column(Integer, default=None)
    chemistry_instrument = Column(Integer, default=None)
    home_instrument = Column(Integer, default=None)
    combine_instrument = Column(Integer, default=None)
    com_lab_morning = Column(Integer, default=None)
    com_no_morning = Column(Integer, default=None)
    student_morning = Column(Integer, default=None)
    com_lab_evening = Column(Integer, default=None)
    com_no_evening = Column(Integer, default=None)
    student_evening = Column(Integer, default=None)
    internet_morning = Column(Integer, default=None)
    internet_evening = Column(Integer, default=None)
    classrooms = Column(Integer, default=None)
    classes = Column(Integer, default=None)
    sections = Column(Integer, default=None)
    openair_class = Column(Integer, default=None)


class BasicFacilities(QueryMixin):
    __tablename__ = 'BasicFacilities'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    emiscode = Column(Integer, ForeignKey('School.emiscode'), primary_key=True)
    drink_water = Column(Integer, default=None)
    drink_water_type = Column(Integer, default=None)
    electricity = Column(Integer, default=None)
    electricity_reasons = Column(Integer, default=None)
    toilets = Column(Integer, default=None)
    toilets_total = Column(Integer, default=None)
    toilet_usable = Column(Integer, default=None)
    toilet_needrepair = Column(Integer, default=None)
    toilet_teachers = Column(Integer, default=None)
    boundary_wall = Column(Integer, default=None)
    bwall_complete = Column(Integer, default=None)
    main_gate = Column(Integer, default=None)
    sewerage = Column(Integer, default=None)


class SportsFacilities(QueryMixin):
    __tablename__ = 'SportsFacilities'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    emiscode = Column(Integer, ForeignKey('School.emiscode'), primary_key=True)
    play_ground = Column(Integer, default=None)
    circket = Column(Integer, default=None)
    football = Column(Integer, default=None)
    hockey = Column(Integer, default=None)
    badminton = Column(Integer, default=None)
    volleyball = Column(Integer, default=None)
    table_tennis = Column(Integer, default=None)
    other = Column(Integer, default=None)

