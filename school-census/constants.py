"""
This module contains global constants for this project.
"""
COMPLETED_FILE_NAME_PATTERN = 'completed_*.xlsx'
EMISCODE_KEY = 'emiscode'
FAILURE_CODE_LABEL = 0
PARSE_DATA_KEY = 'parse_data'
UPDATE_DATA_KEY = 'update_data'
SUCCESS_CODE_LABEL = 1
SCRAPE_WEB_URL = (
    'http://schoolportal.punjab.gov.pk/SchCriteriaEmisCode.asp?myemiscode=%s')
SCRAPE_FIELDS = [
    {'field_to_scrape':'TOTAL:', 'db_field': 'total_no_of_students',
     'model_class_name': 'Enrollment'}]

SCHOOL_FIELDS = [
    'emiscode', 'school_name', 'dist_id', 'dist_nm', 'teh_id', 'teh_nm',
    'markazid', 'markaznm', 'muza', 'address', 'village_mohallah', 'uc_name',
    'uc_no', 'pp_no', 'na_no', 'head_name', 'nidc_no', 'head_charge',
    'head_grade', 'resident_phone', 'mobile_phone', 'school_phone',
    'school_email', 'contact_no', 'school_status', 'non_func_reason', 'medium',
    'school_shift', 'school_location', 'gender_register', 'school_gender',
    'gender_studying', 'school_level', 'consolidation_status', 'school_type',
    'est_year', 'upgrade_year_pri', 'upgrade_year_mid', 'upgrade_year_high',
    'upgrade_year_hsec', 'bldg_status', 'bldg_ownship', 'place_status',
    'construct_type', 'new_construct_year', 'bldg_condition', 'area_kanal',
    'area_marla', 'covered_area', 'uncover_kanal', 'uncover_marla',
    'flood_affected', 'flood_type', 'po_bank_name', 'sc_ac_no', 'ac_open_date',
    'ftf_collection', 'govt_receive', 'non_govt_receive', 'amount_before',
    'amount_after', 'expenses', 'sc_meetings', 'sc_total', 'sc_women', 'sc_men',
    'parent_member', 'teacher_member', 'general_member', 'new_construct',
    'nsb_bank_name', 'nsb_ac_no', 'nsb_ac_date', 'nsb_before', 'nsb_receive',
    'nsb_after', 'nsb_expenditure', 'dev_plan_date', 'doc']
ENROLLMENT_FIELDS = [
    'eng_kachi_b', 'eng_kachi_g', 'eng_cls1_b', 'eng_cls1_g', 'eng_cls2_b',
    'eng_cls2_g', 'eng_cls3_b', 'eng_cls3_g', 'eng_cls4_b', 'eng_cls4_g',
    'eng_cls5_b', 'eng_cls5_g', 'eng_cls6_b', 'eng_cls6_g', 'eng_cls7_b',
    'eng_cls7_g', 'eng_cls8_b', 'eng_cls8_g', 'eng_cls9_b', 'eng_cls9_g',
    'eng_cls10_b', 'eng_cls10_g', 'cs_cls9', 'cs_cls10', 'bio_cls9',
    'bio_cls10', 'ee_kachi', 'ee_cls1', 'ee_cls2', 'ee_cls3', 'ee_cls4',
    'ee_cls5', 'ee_other', 'emiscode']
ACADEMIC_FACILITIES_FIELDS = [
    'teacher_nofurniture', 'student_nofurniture', 'library', 'if_yes',
    'total_books', 'lab_exist', 'physics_lab', 'biology_lab', 'chemistry_lab',
    'homeconomics_lab', 'combine_lab', 'physics_instrument',
    'biology_instrument', 'chemistry_instrument', 'home_instrument',
    'combine_instrument', 'com_lab_morning', 'com_no_morning',
    'student_morning', 'com_lab_evening', 'com_no_evening', 'student_evening',
    'internet_morning', 'internet_evening', 'classrooms', 'classes',
    'sections', 'openair_class', 'emiscode']
BASIC_FACILITIES_FIELDS = [
    'drink_water', 'drink_water_type', 'electricity', 'electricity_reasons',
    'toilets', 'toilets_total', 'toilet_usable', 'toilet_needrepair',
    'toilet_teachers', 'boundary_wall', 'bwall_complete', 'main_gate',
    'sewerage', 'emiscode']
SPORTS_FACILITIES_FIELDS = ['emiscode', 'play_ground', 'circket', 'football',
                            'hockey', 'badminton', 'volleyball', 'table_tennis',
                            'other']
TEACHING_STAFF_FIELDS = ['emiscode', 'sanctioned', 'filled']