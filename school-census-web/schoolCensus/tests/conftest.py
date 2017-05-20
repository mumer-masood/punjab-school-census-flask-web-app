# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from schoolCensus.app import create_app
from schoolCensus.database import db as _db
from schoolCensus.settings import TestConfig

from .factories import UserFactory


@pytest.yield_fixture(scope='session')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='session')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db):
    """Sets up database session for a test. Returns a db session object. In tear
    down delete test data form database tables.
    """
    yield db.session

    # Delete tables in reverse order. This should ensure that children are
    # deleted before parents
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

@pytest.fixture
def user(session):
    """A user for the tests."""
    user = UserFactory(password='myprecious')
    session.commit()
    return user
