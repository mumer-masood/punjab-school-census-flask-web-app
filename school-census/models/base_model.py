"""
This is the BaseModel module. All model classes inherits QueryMixin base class,
so no need to implement following methods in all model classes.
    1- get
    2- get_by_id
    3- save
    4- delete
    5- update
    6- get_all
"""
import logging
from sqlalchemy.orm.exc import NoResultFound

from db import db_session, Alchemy_Base, DB


LOGGER = logging.getLogger(__file__)


class classproperty(object):
    def __init__(self, getter_func):
        self.getter_func = getter_func

    def __get__(self, instance, owner_class):
        return self.getter_func(owner_class)


class QueryMixin(Alchemy_Base, object):
    """
    This is BaseModel class. This class has following methods:
    1- get
    2- get_by_id
    3- save
    4- delete
    5- update
    6- get_all
    All model classes inherits this base class, so no need to implement above
    mentioned methods in all model classes.
    """
    __abstract__ = True

    query = db_session.query_property()

    def to_json(self):
        """
        Converts SqlAlchemy object to serializable dictionary

        Some data types are not json serializable e.g. DATETIME, TIMESTAMP
        so we are making a dictionary where keys are types and values are types to which we want to
        convert this data.
        """
        # add your conversions for things like datetime's
        # and what-not that aren't serializable.
        convert = dict(DATETIME=str, TIMESTAMP=str,
                       DATE=str, TIME=str)
        # data dictionary which will contain add data for this instance
        data = dict()
        # iterate through all columns key, values
        for col in self.__class__.__table__.columns:
            # if name is in camel case convert it to snake case
            name = col.name
            # get value against this column name
            value = getattr(self, name)
            # get column type and check if there as any conversion method given for that type.
            # if it is, then use that method or type for data conversion
            typ = str(col.type)
            if typ in convert.keys() and value is not None:
                try:
                    # try to convert column value by given converter method
                    data[name] = convert[typ](value)
                except:
                    data[name] = "Error:  Failed to covert using ", str(convert[typ])
            elif value is None:
                # if value is None, make it empty string
                data[name] = str()
            else:
                # it is a normal serializable column value so add to data dictionary as it is.
                data[name] = value
        return data

    @classproperty
    def session(cls):
        return db_session

    @classmethod
    def get(cls, pk_id):
        """
        This method gets object from database against given id.
        If that object is already in session, this method will not get that
        object from database.
        This function will raise NoResultFound exception if no record found in
        database against given primary key.
        """
        obj = cls.query.get(pk_id)
        if not obj:
            raise NoResultFound
        return obj

    @classmethod
    def get_by_id(cls, pk_id):
        """
        This method gets the latest object from database against given id.
        """
        primary_key = cls.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key
        return cls.query.filter(filter_string).params(value=pk_id).first()

    @classmethod
    def get_all(cls):
        """Return all records of calling class."""
        return cls.query.all()

    @classmethod
    def save(cls, instance):
        """
        Take object of model class and save that object in database.
        """
        cls.session.add(instance)
        # cls.session.commit()

    @classmethod
    def delete(cls, pk_id):
        """
        This method gets object against given primary key and delete it from
        database.
        """
        primary_key = cls.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key
        rows_deleted = cls.query.filter(filter_string).params(value=pk_id).delete('fetch')

        # if rows_deleted:
        #     cls.session.commit()
        return rows_deleted

    def update(self, **args):
        """
        1) This methods gets primary key of table of current object.
        2) Make filter string using that primary key.
        3) Finally update current record with given values in args dictionary.

        Note:
        'fetch' string is passed in update function so that it will also update
        object in current session.
        """
        assert args, "No argument given to update method to update this object"
        primary_key = self.__mapper__.primary_key[0].key
        # We used this to avoid Sql injection
        filter_string = '%s = :value' % primary_key
        rows_updated = self.query.filter(filter_string).params(
            value=getattr(self, primary_key)).update(args, 'fetch')
        # if args['commit']:
        #     self.session.commit()
        return rows_updated

    # def get_access_cls(cls, key):
    #     """"""
    #     if key in cls.metadata.tables:
    #         return cls.metadata.tables[key]
        # elif key in cls.metadata._schemas:
        #     return _GetTable(key, cls.metadata)
        # else:
        #     return sqlalchemy.__dict__[key]

def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for _class in Alchemy_Base._decl_class_registry.values():
        if hasattr(_class, '__tablename__') and _class.__tablename__ == tablename:
            return _class

def create_db_schema():
    """"""
    Alchemy_Base.metadata.create_all(bind=DB)

def drop_db_schema():
    """"""
    Alchemy_Base.metadata.drop_all(bind=DB)