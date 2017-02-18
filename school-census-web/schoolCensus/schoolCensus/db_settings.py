"""

"""

DEV_DATABASE_CREDENTIALS = {
        'NAME': 'punjab_school_census',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'}

PROD_DATABASE_CREDENTIALS = {
        'NAME': 'wyounas$school_census',
        'USER': 'wyounas',
        'PASSWORD': 'schoolcensus',
        'HOST': 'wyounas.mysql.pythonanywhere-services.com',
        'PORT': '3306'}

TEST_DATABASE_CREDENTIALS = {
        'NAME': 'punjab_school_census',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'}

DEV_DB_URI = 'mysql://%s:%s@%s:%s/%s' % (DEV_DATABASE_CREDENTIALS['USER'],
                                         DEV_DATABASE_CREDENTIALS['PASSWORD'],
                                         DEV_DATABASE_CREDENTIALS['HOST'],
                                         DEV_DATABASE_CREDENTIALS['PORT'],
                                         DEV_DATABASE_CREDENTIALS['NAME'])

PROD_DB_URI = 'mysql://%s:%s@%s:%s/%s' % (PROD_DATABASE_CREDENTIALS['USER'],
                                          PROD_DATABASE_CREDENTIALS['PASSWORD'],
                                          PROD_DATABASE_CREDENTIALS['HOST'],
                                          PROD_DATABASE_CREDENTIALS['PORT'],
                                          PROD_DATABASE_CREDENTIALS['NAME'])

TEST_DB_URI = 'mysql://%s:%s@%s:%s/%s' % (TEST_DATABASE_CREDENTIALS['USER'],
                                          TEST_DATABASE_CREDENTIALS['PASSWORD'],
                                          TEST_DATABASE_CREDENTIALS['HOST'],
                                          TEST_DATABASE_CREDENTIALS['PORT'],
                                          TEST_DATABASE_CREDENTIALS['NAME'])