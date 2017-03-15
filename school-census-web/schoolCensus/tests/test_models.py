# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from schoolCensus.user.models import Role, User

from .factories import UserFactory


class TestUser:
    """User tests."""

    def test_get_by_id(self, session):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        session.add(user)
        session.commit()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self, session):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        session.add(user)
        session.commit()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self, session):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        session.add(user)
        session.commit()
        assert user.password is None

    def test_factory(self, session):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        session.add(user)
        session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    @pytest.mark.usefixtures('session')
    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    @pytest.mark.usefixtures('session')
    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self, session):
        """Add a role to a user."""
        role = Role(name='admin')
        session.add(role)
        session.commit()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles
