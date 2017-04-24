INITIAL_ALL = 'all'

EQUAL_OP = 'equal'
LESS_THAN_OP = 'less than'
LESS_THAN_EQUAL_TO_OP = 'less than equal to'
GREATER_THAN_OP = 'greather than'
GREATER_THAN_EQUAL_OP = 'greather than equal to'
IN_OP = 'in'
NOT_OP = 'not equal'
AND_OP = 'and'
OR_OP = 'or'
SUM_OP = 'sum'

SAME_TABLE_SIMPLE_CHART = 'same_table_simple_chart'
JOIN_TABLE_SIMPLE_CHART = 'join_table_simple_chart'
JOIN_TABLE_PERCENTAGE_CHART = 'join_table_percentage_chart'
JOIN_TABLE_RATIO_CHART = 'join_table_ratio_chart'

FIELD_MODEL_LABEL = 'field_model'
PERCENTAGE_LABEL = 'percentage'
OPERATOR_FIELDS = 'operator_fields'

# Following dictionary contains charts configrations, each chart has integer id
# defined as a main dictionary key

CHART_DATA = {
    1: {'chart_label': 'New Construction',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_schools_by_new_construction',
        'criteria': {'field_name': 'new_construct_year', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District', 'No New Construction Made',
                              'New Construction Made']
        },
    2: {'chart_label': 'Construction Made Before 2000',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_school_constructed_before_2000',
        'criteria': {'field_name': 'new_construct_year', 'value': 2000,
                     'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Construction Made Before 2000',
                              'Construction Made After 2000']},
    3: {'chart_label': 'No School Meetings',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_school_with_no_school_meetings',
        'criteria': {'field_name': 'sc_meetings', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District', 'No School Meetings Conducted',
                              'School Meetings Conducted']
        },
    4: {'chart_label': 'Less than 10 School Meetings',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_school_with_less_than_10_school_meetings',
        'criteria': {'field_name': 'sc_meetings', 'value': 10,
                     'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Less than 10 School Meetings Conducted',
                              'More than 10 School Meetings Conducted']
        },
    5: {'chart_label': 'No School Women',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_school_without_female_member_in_school_council',
        'criteria': {'field_name': 'sc_women', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'No Women in Schools',
                              'Women in Schools']
        },
    6: {'chart_label': 'No School Men',
        'type': SAME_TABLE_SIMPLE_CHART,
        'method': 'get_school_without_male_member_in_school_council',
        'criteria': {'field_name': 'sc_men', 'value': 0, 'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'No Men in Schools',
                              'Men in Schools']
        },
    7: {'chart_label': 'Schools with Less than 4 Classrooms',
        'type': JOIN_TABLE_SIMPLE_CHART,
        'method': 'get_school_with_less_than_four_classrooms',
        'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                     'field_name': 'classrooms', 'value': 4,
                     'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Schools with Less than 4 Classrooms',
                              'Schools with More than 4 Classrooms']
        },
    8: {'chart_label': 'Schools with at least 1 Open Air Class',
        'type': JOIN_TABLE_SIMPLE_CHART,
        'method': 'get_school_with_one_open_air_class',
        'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                     'field_name': 'openair_class', 'value': 1,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Schools with at least 1 Open Air Class',
                              'Schools with No Open Air Class']
        },
    9: {'chart_label': 'Schools have Less than 50% usable toilets',
        'type': JOIN_TABLE_PERCENTAGE_CHART,
        'method': 'get_school_with_less_than_fifty_percet_usable_toilets',
        'criteria': {FIELD_MODEL_LABEL: 'BasicFacilities',
                     'field_name': 'toilet_usable',
                     'total_field_name': 'toilets_total',
                     'value': 50, 'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Schools have Less than 50% usable toilets',
                              'Schools have More than 50% usable toilets']
        },
    10: {'chart_label': 'Schools with No Hockey Facility',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_schools_without_facilities_for_hockey',
         'criteria': {FIELD_MODEL_LABEL: 'SportsFacilities',
                      'field_name': 'hockey', 'value': 0, 'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools with No Hockey Facility',
                               'Schools have Hockey Facility']
         },
    11: {'chart_label': 'School with Less than 100 Books',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_school_with_less_than_hundred_books',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'field_name': 'total_books', 'value': 100,
                      'operator': LESS_THAN_EQUAL_TO_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have Less than 100 Books',
                               'Schools have More than 100 Books']
         },
    12: {'chart_label': 'Schools have No Labs',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_schools_without_lab',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'field_name': 'lab_exist', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have No Labs',
                               'Schools have Labs']},
    13: {'chart_label': 'Schools have No Internet',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_school_without_internet_access',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'operator': OR_OP,
                      OPERATOR_FIELDS: [
                          {'field_name': 'internet_morning', 'value': 1,
                           'operator': EQUAL_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'},
                          {'field_name': 'internet_evening', 'value': 1,
                           'operator': EQUAL_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'}]},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District', 'Schools have No Internet',
                               'Schools have Internet']},
    14: {'chart_label': 'Schools have Physics Labs with No Instruments',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_schools_with_physics_lab_and_without_instrument',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'operator': AND_OP,
                      OPERATOR_FIELDS: [
                          {'field_name': 'physics_lab', 'value': 1,
                           'operator': EQUAL_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'},
                          {'field_name': 'physics_instrument', 'value': 3,
                           'operator': NOT_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'}]},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have Physics Labs with No Instruments',
                               'Schools have Physics Labs with Instruments']},
    15: {'chart_label': 'Schools have Chemistry Labs with No Instruments',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_school_with_chemistry_lab_and_without_instrument',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'operator': AND_OP,
                      OPERATOR_FIELDS: [
                          {'field_name': 'chemistry_lab', 'value': 1,
                           'operator': EQUAL_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'},
                          {'field_name': 'chemistry_instrument', 'value': 3,
                           'operator': NOT_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'}]},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have Chemistry Labs with No Instruments',
                               'Schools have Chemistry Labs with Instruments']},
    16: {'chart_label': 'Schools have Biology Labs with No Instruments',
         'type': JOIN_TABLE_SIMPLE_CHART,
         'method': 'get_school_with_biology_lab_and_without_instrument',
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'operator': AND_OP,
                      OPERATOR_FIELDS: [
                          {'field_name': 'biology_lab', 'value': 1,
                           'operator': EQUAL_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'},
                          {'field_name': 'biology_instrument', 'value': 3,
                           'operator': NOT_OP,
                           'operation': OR_OP,
                           'query_class': 'AcademicFacilities'}]},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have Biology Labs with No Instruments',
                               'Schools have Biology Labs with Instruments']},
    17: {'chart_label': 'Schools have No English Medium Students',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_urdu_medium_schools',
         'criteria': {'field_name': 'medium', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': [
             'District', 'Schools have No English Medium Students',
             'Schools have English Medium Students']
         },
    18: {'chart_label': 'Non Functional Schools',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_non_functional_schools',
         'criteria': {'field_name': 'school_status', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Non Functional Schools',
                               'Rest of Schools']
         },
    19: {'chart_label': 'Schools closed because of No Teachers',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_closed_due_to_teachers_nonavailability',
         'criteria': {'field_name': 'non_func_reason', 'value': 1,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Teachers',
                               'Rest of Schools']
         },
    20: {'chart_label': 'Schools closed because of No Students',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_closed_due_to_students_nonavailability',
         'criteria': {'field_name': 'non_func_reason', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Students',
                               'Rest of Schools']
         },
    21: {'chart_label': 'Schools closed because of No Building',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_closed_due_to_building_nonavailability',
         'criteria': {'field_name': 'non_func_reason', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Building',
                               'Rest of Schools']
         },
    22: {'chart_label': 'Schools closed because of Occupied Building',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_closed_due_to_building_occupied',
         'criteria': {'field_name': 'non_func_reason', 'value': 4,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of Occupied Building',
                               'Rest of Schools']
         },
    23: {'chart_label': 'Schools Building Need Partial Renovation',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_with_building_require_partial_renovation',
         'criteria': {'field_name': 'bldg_status', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building Need Partial Renovation',
                               'Rest of Schools']
         },
    24: {'chart_label': 'Schools Building Need Full Renovation',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_with_building_require_full_renovation',
         'criteria': {'field_name': 'bldg_status', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building Full Partial Renovation',
                               'Rest of Schools']
         },
    25: {'chart_label': 'Schools Building is Partially Dangerous',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_with_building_condition_partially_dangerous',
         'criteria': {'field_name': 'bldg_status', 'value': 5,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building is Partially Dangerous',
                               'Rest of Schools']
         },
    26: {'chart_label': 'Schools Building is Fully Dangerous',
         'type': SAME_TABLE_SIMPLE_CHART,
         'method': 'get_schools_with_building_condition_fully_dangerous',
         'criteria': {'field_name': 'bldg_status', 'value': 4,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building is Fully Dangerous',
                               'Rest of Schools']
         },
    27: {'chart_label': 'Schools Students Teacher Ratio',
         'type': JOIN_TABLE_RATIO_CHART, 'js_chart_type': None,
         'all_districts_chart_title_fields': ['Chart Field',
                                              'Number of Students Per Teacher'],
         'all_districts_chart_data_fields': ['District',
                                             'District Students Per Teacher']},
}

NO_NEW_CONSTRUCTION = 0
YEAR_TWO_THOUSAND = 2000
NO_SCHOOL_MEETINGS = 0
TEN_SCHOOL_MEETING = 10
NO_FEMALE_MEMBER = 0
NO_MALE_MEMBER = 0
FOUR_CLASSROOMS = 4
ONE_OPEN_AIR_CLASS = 1
NO_HOCKEY = 0
HUNDRED = 100
NO_PHY_LAB_INS = 3
NO_CHE_LAB_INS = 3
NO_BIO_LAB_INS = 3
FIFTY = 50
PERMANENT_HEAD_CHARGE = 1
ADDITIONAL_HEAD_CHARGE = 2
LOOKAFTER_HEAD_CHARGE = 3
FUNCTIONAL_SCHOOLS = 1
NON_FUNCTIONAL_SCHOOLS = 2
MERGED_SCHOOLS = 3
DENOTIFIED_SCHOOLS = 4
CONSOLIDATED_SCHOOLS = 5
ENGLISH_MEDIUM = 1
URDU_MEDIUM = 2
ENGLISH_AND_URDU_MEDIUM = 3
MORNING_SHIFT = 1
EVENING_SHIF = 2
URBAN_SCHOOLS = 1
RURAL_SCHOOLS = 2
TEACHERS_NOT_AVAILABLE = 1
STUDENT_NOT_AVAILABLE = 2
BUILDING_NOT_AVAILABLE = 3
BUILDING_OCCUPIED = 4
BOYS_SCHOOLS = 1
GIRLS_SCHOOLS = 2
BOYS_STUDYING = 1
GIRLS_STUDYING = 2
GIRLS_AND_BOYS_STUDYING = 3
KEY_SMOSQUE = 'sMosque'
KEY_PRIMARY = 'Primary'
KEY_MIDDLE = 'Middle'
KEY_HIGH = 'High'
KEY_HIGHER_SECONDARY = 'H.Sec.'
COMMUNITY_MODEL_SCHOOLS = 1
JUNIOR_MODEL_SCHOOLS = 2
PILOT_SECONDARY_SCHOOLS = 3
COMPREHENSIVE_SCHOOLS = 4
TECH_HIGH_SCHOOLS = 5
MODEL_SCHOOLS = 6
LOCAL_GOVT_SCHOOLS = 7
WITH_BUILDING = 1
WITHOUT_BUILDING = 2
EDUCATION_DEPARTMENT_BUILDING = 1
ANOTHER_SCHOOL_BUILDING = 2
ON_LEASE_BUILDING = 3
LOCAL_POPULATION_BUILDING = 4
MUNICIPAL_CORPORATION_BUILDING = 5
SCHOOL_COUNCIL_BUILDING = 6
NON_MUNICIPAL_CORPORATION_BUILDING = 7
MOSQUE_BUILDING = 8
GOVT_ALLOCATED_PLACE = 1
NOT_GOVT_ALLOCATED_PLACE = 2
MUD = 1
CONCRETE = 2
MUD_AND_CONCRETE = 3
STABLE_BUILDING = 1
SOME_REPAIRMENT = 2
FULL_REPAIRMENT = 3
FULLY_DANGEROUS_BUILDING = 4
PARTIALLY_DANGEROUS_BUILDING = 5
DRINKING_WATER_AVAILABLE = 1
DRINKING_WATER_NOT_AVAILABLE = 2
DRINKING_WATER_NOT_WORKING = 3
WELL = 1
HAND_PUMP = 2
WATER_PUMP = 3
GOVT_NULL = 4
OTHER_WATER_TYPE = 5
WITH_ELECTRICITY = 1
WITHOUT_ELECTRICITY = 2
ELECTRICITY_NOT_WORKING = 3
UNPAID_BILL = 1
FAULTY_WIRING = 2
NO_CONNECTION = 3
WITH_TOILETS = 1
WITHOUT_TOILETS = 2
NONFUNCTIONAL_TOILETS = 3
BOUNDARY_WALL = 1
WITHOUT_BOUNDARY_WALL = 2
COMPLETE_BOUNDARY_WALL = 1
INCOMPLETE_BOUNDARY_WALL = 2
BAD_BOUNDARY_WALL = 3
MAIN_GATE = 1
WITHOUT_MAIN_GATE = 2
SEWERAGE_SYSTEM = 1
NO_SEWERAGE_SYSTEM = 2
PLAYGROUND = 1
NO_PLAYGROUND = 2
CRICKET = 1
FOOTBALL = 1
HOCKEY = 1
BADMINTON = 1
VOLLEY_BALL = 1
TABLE_TENNIS = 1
OTHER_SPORTS = 1
LIBRARY = 1
NO_LIBRARY = 2
LAB = 1
NO_LAB = 2
PHYSICS_LAB = 1
NO_PHYSICS_LAB = 2
BIOLOGY_LAB = 1
NO_BIOLOGY_LAB = 2
CHEMISTRY_LAB = 1
NO_CHEMISTRY_LAB = 2
HOME_ECONOMICS_LAB = 1
NO_HOME_ECONOMICS_LAB = 2
COMBINE_LAB = 1
NO_COMBINE_LAB = 2
PHYSICS_LAB_INSTRUMENT = 1
NO_PHYSICS_LAB_INSTRUMENT = 2
BIOLOGY_LAB_INSTRUMENT = 1
NO_BIOLOGY_LAB_INSTRUMENT = 2
CHEMISTRY_LAB_INSTRUMENT = 1
NO_CHEMISTRY_LAB_INSTRUMENT = 2
HOME_ECONOMICS_LAB_INSTRUMENT = 1
NO_HOME_ECONOMICS_LAB_INSTRUMENT = 2
COMBINE_LAB_INSTRUMENT = 1
NO_COMBINE_LAB_INSTRUMENT = 2
MORNING_COMPUTER_LAB = 1
NO_MORNING_COMPUTER_LAB = 2
EVENING_COMPUTER_LAB = 1
NO_EVENING_COMPUTER_LAB = 2
INTERNET_ACCESS_MORNING = 1
NO_INTERNET_ACCESS_MORNING = 2
INTERNET_ACCESS_EVENING = 1
NO_INTERNET_ACCESS_EVENING = 2

