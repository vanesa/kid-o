from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

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
    confirm = PasswordField('Repeat Password')

class ChildForm(Form):
    first_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    last_name = StringField('first_name', validators=[DataRequired(), Length(max=15)])
    # birth_date = request.form.get("birth_date")
    # guardian_type = request.form.get("guardian_type")
    # guardian_fname = request.form.get("guardian_fname")
    # guardian_lname = request.form.get("guardian_lname")
    # medical_condition = request.form.get("medical_condition")
    # doctor_appt = request.form.get("doctor_appt")
    # situation = request.form.get("situation")
    # home_visit = request.form.get("home_visit")
    # latitude = request.form.get("latitude")
    # longitude = request.form.get("longitude")
