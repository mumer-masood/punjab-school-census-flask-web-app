from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, scoped_session

from settings import DATABASE_CREDENTIALS


Alchemy_Base = declarative_base()
DB = create_engine('mysql://%s:%s@%s:%s/%s' % (DATABASE_CREDENTIALS['USER'],
                                               DATABASE_CREDENTIALS['PASSWORD'],
                                               DATABASE_CREDENTIALS['HOST'],
                                               DATABASE_CREDENTIALS['PORT'],
                                               DATABASE_CREDENTIALS['NAME']),
                   pool_size = 10, pool_recycle=100)
db_session = scoped_session(session.sessionmaker(bind=DB, expire_on_commit=False))
alchemy_session = db_session
META = MetaData(DB)