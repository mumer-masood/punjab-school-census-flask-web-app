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
    chart_type = chart_criteria.get('js_chart_type')
    _response = {'chart_data': chart_data}
    if chart_type:
        _response['chart_type'] = chart_type
    return jsonify(_response)


def get_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :return:
    """
    assert chart_criteria is not None
    chart_data = None
    if chart_criteria['type'] == constants.SAME_TABLE_SIMPLE_CHART:
       chart_data = get_same_table_chart_data(chart_criteria)
    if chart_criteria['type'] == constants.JOIN_TABLE_SIMPLE_CHART:
        chart_data = get_join_table_chart_data(chart_criteria)
    if chart_criteria['type'] == constants.JOIN_TABLE_PERCENTAGE_CHART:
        chart_data = get_join_table_percentage_chart_data(chart_criteria)
    if chart_criteria['type'] == constants.JOIN_TABLE_RATIO_CHART:
        chart_data = get_join_table_ratio_chart_data(chart_criteria)

    return chart_data


def get_join_table_ratio_chart_data(chart_criteria):
    """"""
    dist_id = request.values.get('dist_id', None)
    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data = get_all_districts_chart_data(chart_criteria)
    else:
        chart_data = get_district_chart_data(chart_criteria, dist_id)

    return chart_data


def get_all_districts_chart_data(chart_criteria):
    """"""
    chart_data = []
    chart_data.append(
        [chart_criteria['all_districts_chart_data_fields'][0].title(),
         chart_criteria['all_districts_chart_data_fields'][1].title()])
    for dist_id, dist_name in models.School.get_districts():
        students_ratio = (
            models.School.district_schools_students_teacher_ratio(dist_id))
        chart_data.append([dist_name.title(), students_ratio])
    chart_criteria['js_chart_type'] = 'bar'
    return chart_data


def get_district_chart_data(chart_criteria, dist_id):
    """"""
    chart_data = []
    chart_data = models.School.district_each_school_students_teacher_ratio(
        dist_id)
    chart_criteria['js_chart_type'] = 'line'
    return chart_data


def get_same_table_chart_data(chart_criteria):
    """

    :param chart_criteria:
    :param request:
    :return:
    """
    chart_data = []
    dist_id = request.values.get('dist_id', None)

    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data.append([chart_criteria['chart_data_fields'][0].title(),
                           chart_criteria['chart_data_fields'][1].title(),
                           chart_criteria['chart_data_fields'][2].title()])
        for dist_id, dist_name in models.School.get_districts():
            field_count = models.School.get_same_table_count(
                district_id=dist_id, criteria=chart_criteria['criteria'],
                count_all=False)
            all_count = models.School.get_same_table_count(
                criteria=chart_criteria['criteria'],
                district_id=dist_id, count_all=True)
            all_count = all_count - field_count
            chart_data.append([dist_name.title(), field_count, all_count])
    else:
        dist_id, dist_name = models.School.get_districts(dist_id)
        field_count = models.School.get_same_table_count(
                district_id=dist_id, criteria=chart_criteria['criteria'],
                count_all=False)
        all_count = models.School.get_same_table_count(
            criteria=chart_criteria['criteria'],
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

    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data.append([chart_criteria['chart_data_fields'][0].title(),
                           chart_criteria['chart_data_fields'][1].title(),
                           chart_criteria['chart_data_fields'][2].title()])
        for dist_id, dist_name in models.School.get_districts():
            field_count = models.School.get_join_table_count(
                criteria=chart_criteria['criteria'],
                district_id=dist_id, count_all=False)
            all_count = models.School.get_join_table_count(
                criteria=chart_criteria['criteria'],
                district_id=dist_id, count_all=True)
            all_count = all_count - field_count
            chart_data.append([dist_name.title(), field_count, all_count])
    else:
        dist_id, dist_name = models.School.get_districts(dist_id)
        field_count = models.School.get_join_table_count(
            criteria=chart_criteria['criteria'],
            district_id=dist_id, count_all=False)
        all_count = models.School.get_join_table_count(
            criteria=chart_criteria['criteria'],
            district_id=dist_id, count_all=True)
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
    chart_data = []
    dist_id = request.values.get('dist_id', None)
    if dist_id == constants.INITIAL_ALL or dist_id is None:
        chart_data.append([chart_criteria['chart_data_fields'][0].title(),
                           chart_criteria['chart_data_fields'][1].title(),
                           chart_criteria['chart_data_fields'][2].title()])
        for dist_id, dist_name in models.School.get_districts():
            field_count = models.School.get_join_table_percentage_count(
                district_id=dist_id, criteria=chart_criteria['criteria'],
                count_all=False)
            all_count = models.School.get_join_table_percentage_count(
                district_id=dist_id, criteria=chart_criteria['criteria'],
                count_all=True)
            all_count = all_count - field_count
            chart_data.append([dist_name.title(), field_count, all_count])
    else:
        dist_id, dist_name = models.School.get_districts(dist_id)
        field_count = models.School.get_join_table_percentage_count(
            district_id=dist_id, criteria=chart_criteria['criteria'],
            count_all=False)
        all_count = models.School.get_join_table_percentage_count(
            district_id=dist_id, criteria=chart_criteria['criteria'],
            count_all=True)
        all_count = all_count - field_count
        chart_data.append([chart_criteria['chart_title_fields'][0].title(),
                           chart_criteria['chart_title_fields'][1].title()])
        chart_data.append([chart_criteria['chart_data_fields'][1].title(),
                           field_count])
        chart_data.append([chart_criteria['chart_data_fields'][2].title(),
                           all_count])
    return chart_data
