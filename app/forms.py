from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, DateField, FloatField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, Optional, Regexp
from app import app

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
    photo_url = FileField(u'photo', validators=[Regexp(r'\.jpg$'), Optional()])
    is_active = BooleanField('is_active')
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=15)])
    nick_name = StringField('nick_name', validators=[Length(max=15)])
    birth_date = DateField('birth_date', validators=[DataRequired()])
    nationality = StringField('nationality')
    guardian_type = StringField('guardian_type', validators=[Length(max=15)])
    guardian_fname = StringField('guardian_fname', validators=[Length(max=25)])
    guardian_lname = StringField('guardian_lname', validators=[Length(max=25)])
    number_of_siblings = IntegerField('number_of_siblings', validators=[NumberRange(min=0, max=8)])
    siblings_in_project = StringField('siblings_in_school', validators=[Length(max=40)])
    school_class = StringField('school_class')
    school_attendance = StringField('school_attendance')
    volunteer_task = StringField('volunteer_task')
    situation = StringField('situation')
    godparent_status = StringField('godparent_status')
    latitude = FloatField('latitude', validators=[Optional()])
    longitude = FloatField('longitude', validators=[Optional()])