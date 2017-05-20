# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy.orm import relationship

from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update,
    delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

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
    def delete(cls, pk_id, commit=True):
        """
        This method gets object against given primary key and delete it from
        database.
        """
        primary_key = cls.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key
        rows_deleted = cls.query.filter(filter_string).params(
            value=pk_id).delete('fetch')

        if commit:
            db.session.commit()
        return rows_deleted

    def update(self, commit=True, **args):
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
        if commit:
            db.session.commit()
        return rows_updated


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float, long))),
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)

def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for _class in db._decl_class_registry.values():
        if hasattr(_class, '__tablename__') and _class.__tablename__ == tablename:
            return _class

# def create_db_schema():
#     """"""
#     db.create_all()
#
# def drop_db_schema():
#     """"""
#     db.metadata.drop_all()
#
# # base_model.drop_db_schema()
# create_db_schema()