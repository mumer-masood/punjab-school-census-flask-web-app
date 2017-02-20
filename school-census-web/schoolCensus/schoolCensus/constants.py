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
        'criteria': {'field_name': 'new_construct_year', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District', 'No New Construction Made',
                              'New Construction Made']
        },
    2: {'chart_label': 'Construction Made Before 2000',
        'type': SAME_TABLE_SIMPLE_CHART,
        'criteria': {'field_name': 'new_construct_year', 'value': 2000,
                     'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Construction Made Before 2000',
                              'Construction Made After 2000']},
    3: {'chart_label': 'No School Meetings',
        'type': SAME_TABLE_SIMPLE_CHART,
        'criteria': {'field_name': 'sc_meetings', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District', 'No School Meetings Conducted',
                              'School Meetings Conducted']
        },
    4: {'chart_label': 'Less than 10 School Meetings',
        'type': SAME_TABLE_SIMPLE_CHART,
        'criteria': {'field_name': 'sc_meetings', 'value': 10,
                     'operator': LESS_THAN_EQUAL_TO_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'Less than 10 School Meetings Conducted',
                              'More than 10 School Meetings Conducted']
        },
    5: {'chart_label': 'No School Women',
        'type': SAME_TABLE_SIMPLE_CHART,
        'criteria': {'field_name': 'sc_women', 'value': 0,
                     'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'No Women in Schools',
                              'Women in Schools']
        },
    6: {'chart_label': 'No School Men',
        'type': SAME_TABLE_SIMPLE_CHART,
        'criteria': {'field_name': 'sc_men', 'value': 0, 'operator': EQUAL_OP},
        'chart_title_fields': ['Chart Field', 'Number of Schools'],
        'chart_data_fields': ['District',
                              'No Men in Schools',
                              'Men in Schools']
        },
    7: {'chart_label': 'Schools with Less than 4 Classrooms',
        'type': JOIN_TABLE_SIMPLE_CHART,
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
         'criteria': {FIELD_MODEL_LABEL: 'SportsFacilities',
                      'field_name': 'hockey', 'value': 0, 'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools with No Hockey Facility',
                               'Schools have Hockey Facility']
         },
    11: {'chart_label': 'School with Less than 100 Books',
         'type': JOIN_TABLE_SIMPLE_CHART,
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
         'criteria': {FIELD_MODEL_LABEL: 'AcademicFacilities',
                      'field_name': 'lab_exist', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools have No Labs',
                               'Schools have Labs']},
    13: {'chart_label': 'Schools have No Internet',
         'type': JOIN_TABLE_SIMPLE_CHART,
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
         'criteria': {'field_name': 'medium', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': [
             'District', 'Schools have No English Medium Students',
             'Schools have English Medium Students']
         },
    18: {'chart_label': 'Non Functional Schools',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'school_status', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Non Functional Schools',
                               'Rest of Schools']
         },
    19: {'chart_label': 'Schools closed because of No Teachers',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'non_func_reason', 'value': 1,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Teachers',
                               'Rest of Schools']
         },
    20: {'chart_label': 'Schools closed because of No Students',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'non_func_reason', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Students',
                               'Rest of Schools']
         },
    21: {'chart_label': 'Schools closed because of No Building',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'non_func_reason', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of No Building',
                               'Rest of Schools']
         },
    22: {'chart_label': 'Schools closed because of Occupied Building',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'non_func_reason', 'value': 4,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools closed because of Occupied Building',
                               'Rest of Schools']
         },
    23: {'chart_label': 'Schools Building Need Partial Renovation',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'bldg_status', 'value': 2,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building Need Partial Renovation',
                               'Rest of Schools']
         },
    24: {'chart_label': 'Schools Building Need Full Renovation',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'bldg_status', 'value': 3,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building Full Partial Renovation',
                               'Rest of Schools']
         },
    25: {'chart_label': 'Schools Building is Partially Dangerous',
         'type': SAME_TABLE_SIMPLE_CHART,
         'criteria': {'field_name': 'bldg_status', 'value': 5,
                      'operator': EQUAL_OP},
         'chart_title_fields': ['Chart Field', 'Number of Schools'],
         'chart_data_fields': ['District',
                               'Schools Building is Partially Dangerous',
                               'Rest of Schools']
         },
    26: {'chart_label': 'Schools Building is Fully Dangerous',
         'type': SAME_TABLE_SIMPLE_CHART,
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
