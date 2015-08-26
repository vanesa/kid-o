from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# def myfilter(data):
# 	return data.lower()

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=200)])




        # first_name = request.form.get("first_name")
        # last_name = request.form.get("last_name")
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