# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired

from schoolCensus import constants
from schoolCensus.school_models import models
from schoolCensus.user.models import User


class LoginForm(Form):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True


class SchoolsFilterForm(Form):
    """"""
    district = SelectField('District Name', coerce=unicode,
                            render_kw={'class': 'form-control'})
    school_name = StringField('School Name',
                              render_kw={
                                  'class': 'form-control',
                                  'placeholder': 'Start Typing School Name'})

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(SchoolsFilterForm, self).__init__(*args, **kwargs)
        self.district.choices = []
        self.district.choices.append((constants.INITIAL_ALL,
                                      'All District'))
        districts = models.School.get_districts()
        self.district.choices.extend(districts)
        initial_option = kwargs.get('initial', constants.INITIAL_ALL)
        self.district.initial = [initial_option]


class ChartsForm(Form):
    """"""
    select_chart = SelectField('Select Chart', coerce=unicode,
                            render_kw={'class': 'form-control'},
                               )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ChartsForm, self).__init__(*args, **kwargs)
        self.select_chart.choices = []
        # self.select_chart.choices.append((constants.INITIAL_ALL,
        #                                   'Select Chart'))
        options = [(chart_id, chart_data['chart_label'])
                   for chart_id, chart_data in constants.CHART_DATA.iteritems()]
        options = sorted(options, key=lambda option: option[0])
        self.select_chart.choices.extend(options)
        initial_option = kwargs.get('initial', constants.INITIAL_ALL)
        self.select_chart.initial = [initial_option]
