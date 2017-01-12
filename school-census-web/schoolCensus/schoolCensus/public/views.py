# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, flash, redirect, render_template, jsonify,
                   request, url_for)
from flask_login import login_required, login_user, logout_user

from schoolCensus import constants
from schoolCensus.extensions import login_manager
from schoolCensus.public.forms import LoginForm, SchoolsFilterForm, ChartsForm
from schoolCensus.user.forms import RegisterForm
from schoolCensus.user.models import User
from schoolCensus.utils import flash_errors
from schoolCensus.school_models import models

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/schools/', methods=['GET', 'POST'])
@login_required
def schools():
    """School census stats page."""
    # Handle logging in
    filter_form = SchoolsFilterForm()
    if request.method == 'POST':
        pass
    else:
        schools = models.School.get_all()

    return render_template('public/schools.html', schools=schools,
                           filter_form=filter_form)

@blueprint.route('/schools/<int:emiscode>/', methods=['GET'])
@login_required
def school(emiscode):
    """School census stats page."""
    assert emiscode is not None
    # Handle logging in
    school = models.School.get_by_id(emiscode)

    return render_template('public/school.html', school=school)


@blueprint.route('/statistics/', methods=['GET'])
@login_required
def stats():
    """School census stats page."""
    # Handle logging in
    district_filter = SchoolsFilterForm()
    chart_filter = ChartsForm()

    return render_template('public/stats.html',
                           filter_form=district_filter,
                           chart_filter=chart_filter)


@blueprint.route('/charts/<int:chart_id>/', methods=['POST'])
@login_required
def charts(chart_id):
    """School census stats page."""
    assert chart_id is not None
    chart_criteria = constants.CHART_DATA.get(chart_id)
    chart_data = get_chart_data(chart_criteria)
    return jsonify(chart_data)


def get_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :return:
    """
    assert chart_criteria is not None
    chart_data = None
    if constants.FIELD_MODEL_LABEL not in chart_criteria['criteria']:
       chart_data = get_same_table_chart_data(chart_criteria)
    if constants.FIELD_MODEL_LABEL in chart_criteria['criteria']:
        if constants.PERCENTAGE_LABEL in chart_criteria['criteria']:
           chart_data = get_join_table_percentage_chart_data(chart_criteria)
        else:
            chart_data = get_join_table_chart_data(chart_criteria)

    return chart_data


def get_same_table_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :param request:
    :return:
    """
    chart_data = []
    dist_id = request.values.get('dist_id', None)
    field = chart_criteria['criteria']['field_name']
    value = chart_criteria['criteria'].get('value', None)
    count_all = chart_criteria.get('count_all', False)
    lt_operator = chart_criteria['criteria'].get('lt_operator', False)

    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data.append([chart_criteria['chart_data_fields'][0].title(),
                           chart_criteria['chart_data_fields'][1].title(),
                           chart_criteria['chart_data_fields'][2].title()])
        for dist_id, dist_name in models.School.get_districts():
            field_count = models.School.get_same_table_count(
                district_id=dist_id, field=field, value=value,
                count_all=count_all, lt_operator=lt_operator)
            all_count = models.School.get_same_table_count(
                district_id=dist_id, count_all=True)
            all_count = all_count - field_count
            chart_data.append([dist_name.title(), field_count, all_count])
    else:
        dist_id, dist_name = models.School.get_districts(dist_id)
        field_count = models.School.get_same_table_count(
            district_id=dist_id, field=field, value=value,
            count_all=count_all, lt_operator=lt_operator)
        all_count = models.School.get_same_table_count(
            district_id=dist_id, count_all=True)
        all_count = all_count - field_count
        chart_data.append([chart_criteria['chart_title_fields'][0].title(),
                           chart_criteria['chart_title_fields'][1].title()])
        chart_data.append([chart_criteria['chart_data_fields'][1].title(),
                           field_count])
        chart_data.append([chart_criteria['chart_data_fields'][2].title(),
                           all_count])
    return chart_data


def get_join_table_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :return:
    """
    chart_data = []
    dist_id = request.values.get('dist_id', None)
    field = chart_criteria['criteria']['field_name']
    value = chart_criteria['criteria'].get('value', None)
    count_all = chart_criteria.get('count_all', False)
    lt_operator = chart_criteria['criteria'].get('lt_operator', False)
    field_model = chart_criteria['criteria'].get(
        constants.FIELD_MODEL_LABEL, None)

    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data.append([chart_criteria['chart_data_fields'][0].title(),
                           chart_criteria['chart_data_fields'][1].title(),
                           chart_criteria['chart_data_fields'][2].title()])
        for dist_id, dist_name in models.School.get_districts():
            field_count = models.School.get_join_table_count(
                district_id=dist_id, field=field, value=value,
                count_all=count_all, lt_operator=lt_operator,
                join_table=field_model)
            all_count = models.School.get_join_table_count(
                district_id=dist_id, count_all=True, join_table=field_model)
            all_count = all_count - field_count
            chart_data.append([dist_name.title(), field_count, all_count])
    else:
        dist_id, dist_name = models.School.get_districts(dist_id)
        field_count = models.School.get_join_table_count(
            district_id=dist_id, field=field, value=value,
            count_all=count_all, lt_operator=lt_operator,
            join_table=field_model)
        all_count = models.School.get_join_table_count(
            district_id=dist_id, count_all=True, join_table=field_model)
        all_count = all_count - field_count
        chart_data.append([chart_criteria['chart_title_fields'][0].title(),
                           chart_criteria['chart_title_fields'][1].title()])
        chart_data.append([chart_criteria['chart_data_fields'][1].title(),
                           field_count])
        chart_data.append([chart_criteria['chart_data_fields'][2].title(),
                           all_count])
    return chart_data


def get_join_table_percentage_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :return:
    """
    return
