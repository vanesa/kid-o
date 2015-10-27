from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, ValidationError
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
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(max=15)])
    birth_date = DateField('birth_date', validators=[DataRequired()])
    guardian_type = StringField('guardian_type', validators=[Length(max=15)])
    guardian_fname = StringField('guardian_fname', validators=[Length(max=15)])
    guardian_lname = StringField('guardian_lname', validators=[Length(max=15)])
    medical_condition = StringField('medical_condition')
    doctor_appt = DateField('doctor_appt')
    situation = StringField('situation')
    home_visit = DateField('home_visit')
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')
