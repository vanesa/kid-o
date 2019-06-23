# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, IntegerField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, Optional, Regexp
from kido.constants import (
    HAITIAN,
    DOMINICAN,
    HAITIAN_DOMINICAN,
    CHILD_HAS_GODPARENT,
    NO_NEED,
    SEARCHING_GODPARENT,
    KINDERGARTEN,
    PRESCHOOL,
    SCHOOL_BASIC,
    SCHOOL_ADVANCED,
    SPECIAL_SCHOOL,
    ORPHANAGE,
    SAN_SKATE,
    DANCE_GROUP,
    VOLLEYBALL_GROUP,
    ENGLISH_GROUP,
    TUTORING_GROUP,
    PROSALUD,
    PROJECT_UNDETERMINED,
    EXACT,
    ESTIMATED,
)


def lower(data):
    return data.lower() if data else data


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()], filters=[lower])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=200)])


class SignUpForm(Form):
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=15)])
    email = StringField('email', validators=[DataRequired(), Email()], filters=[lower])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=200)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate_confirm(form, field):
        confirm_value = field.data
        password_value = form._fields.get('password').data
        if password_value != confirm_value:
            raise ValidationError('Please type in the same password as in the password field.')


class ChildForm(Form):
    photo = FileField(u'photo', validators=[Regexp(r'\.jpg$'), Optional()])
    is_active = BooleanField('is_active')
    gender = SelectField('gender', validators=[Optional()], choices=[(x, x) for x in ['Male', 'Female']])
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=15)])
    nick_name = StringField('nick_name', validators=[Length(max=15)])
    birth_date = DateField('birth_date', validators=[DataRequired()])
    birth_date_accuracy = SelectField('birth_date_accuracy', validators=[Optional()], choices=[(x, x) for x in [EXACT, ESTIMATED]])
    nationality = SelectField('nationality', validators=[Optional()], choices=[(x, x) for x in [HAITIAN, DOMINICAN, HAITIAN_DOMINICAN]])
    guardian_type = StringField('guardian_type', validators=[Length(max=15)])
    guardian_fname = StringField('guardian_fname', validators=[Length(max=25)])
    guardian_lname = StringField('guardian_lname', validators=[Length(max=25)])
    max_number_of_siblings = 8
    number_of_siblings = IntegerField('number_of_siblings', validators=[NumberRange(min=0, max=max_number_of_siblings)])
    siblings_in_project = StringField('siblings_in_school', validators=[Length(max=40)])
    school_class = SelectField('school_class', validators=[Optional()], choices=[(x, x) for x in [
        KINDERGARTEN, PRESCHOOL, SCHOOL_BASIC, SCHOOL_ADVANCED, SPECIAL_SCHOOL]])
    school_attendance = SelectField('school_attendance', validators=[Optional()], choices=[(x, x) for x in [
        'Good', 'Intermediate', 'Bad'
    ]])
    projects = SelectMultipleField()
    volunteer_task = StringField('volunteer_task')
    situation = StringField('situation')
    godparent_status = SelectField('godparent_status', validators=[Optional()], choices=[(x, x) for x in [
        SEARCHING_GODPARENT, CHILD_HAS_GODPARENT, NO_NEED
    ]])
    latitude = FloatField('latitude', validators=[Optional()])
    longitude = FloatField('longitude', validators=[Optional()])


class GodparentForm(Form):
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=15)])
    referral_name = StringField('referal_name', validators=[Optional(), Length(max=25)])
    email = StringField('email', validators=[DataRequired(), Email()], filters=[lower])


class SearchForm(Form):
    name = StringField(validators=[Optional(), Length(max=25)])
    class_str = SelectField(validators=[Optional()], choices=[(x, x) for x in [
        KINDERGARTEN, PRESCHOOL, SCHOOL_BASIC, SCHOOL_ADVANCED, SPECIAL_SCHOOL]])
    project = SelectField(validators=[Optional()], choices=[(x, x) for x in [
        ORPHANAGE, SAN_SKATE, DANCE_GROUP, VOLLEYBALL_GROUP, ENGLISH_GROUP, TUTORING_GROUP, PROSALUD, PROJECT_UNDETERMINED]])
    show_hidden_profiles = BooleanField('show_hidden_profiles')


class GPSearchForm(Form):
    name = StringField(validators=[Optional(), Length(max=25)])
    child_name = StringField(validators=[Optional(), Length(max=25)])
    project = SelectField(validators=[Optional()], choices=[(x, x) for x in [
        ORPHANAGE, SAN_SKATE, DANCE_GROUP, VOLLEYBALL_GROUP, ENGLISH_GROUP, TUTORING_GROUP, PROSALUD, PROJECT_UNDETERMINED]])
