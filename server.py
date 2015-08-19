""" Kid-O server"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Child, connect_to_db, db
from datetime import datetime

from child import ChildView

app = Flask(__name__)

# Required to use Flask sessions and debug toolbar

app.secret_key = "ABC"

# Raise error if there is an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

#################
# INDEX & LOGIN #
#################

@app.route('/')
def index():
    """" Starting page with either login or personal profile if login session exists.
     For Log in: take email, password from user and check if credentials exist in the database
     by checking if email is in the users table. If email in table, redirect to the children overview.
     If not: redirect to sign up page."""

    if request.method == 'POST': # Process form if route gets POST request from /index
        email = request.form.get("email")
        password = request.form.get("password") #

        credentials = (email, password)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Please sign up!')
            return redirect('/signup')
        else:
            if user.password != password:
                flash('Incorrect password.')
                return redirect('/')

            session['login_id']= credentials # Save session
            flash('You have sucessfully logged in.')
            return redirect("/overview.html") # Redirect to children's overview

    return render_template("index.html")

###########
# LOG OUT #
###########



###########
# SIGN UP #
###########

@app.route('/signup')
def signup_form():
    """ Sign up user """

    return render_template("signup.html")

#####################
# CHILDREN OVERVIEW #
#####################

@app.route('/overview')
def show_overview():
    """ Shows overview of all of the children in the project ordered by lastname."""

    all_children = db.session.query(Child).all() # 
    child_views = []

    for child in all_children:
        child_views.append(ChildView(child))


    return render_template('overview.html', child_profiles=child_views)


##################
# CHILD PROFILE #
#################


@app.route('/child/<int:id>', methods=['GET', 'POST'])
def child_profile(id):
    """ Show's each child's profile with the following information: First name, last name,
    age, birth date, guardian, siblings, medical condition, next doctor's appointment, sitution at
    home and school and when the next home visit is due. """

    if request.method == 'POST': # update child info from edit_profile.html form

        # get all new data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        guardian_fname = request.form.get("guardian_fname")
        guardian_lname = request.form.get("guardian_lname")
        guardian_type = request.form.get("guardian_type")
        medical_condition = request.form.get("medical_condition")
        doctor_appt = request.form.get("doctor_appt")
        situation = request.form.get("situation")
        home_visit = request.form.get("home_visit")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        # seed into database

        child_entry = db.session.query(Child).filter_by(id=id).one()
        child_entry.first_name = first_name
        child_entry.last_name = last_name
        child_entry.birth_date = birth_date
        child_entry.guardian_type = guardian_type
        child_entry.guardian_fname = guardian_fname
        child_entry.guardian_lname = guardian_lname
        child_entry.medical_condition = medical_condition
        child_entry.doctor_appt = doctor_appt
        child_entry.situation = situation
        child_entry.home_visit = home_visit
        child_entry.latitude = latitude
        child_entry.longitude = longitude

        db.session.commit()
        this_child = db.session.query(Child).filter_by(id=id).one()
        child_info = [ChildView(this_child)]

        return render_template('child_profile.html', child_info=child_info)

    else:
        this_child = db.session.query(Child).filter_by(id=id).one()

        child_info = [ChildView(this_child)]

        return render_template('child_profile.html', child_info=child_info)


# Look up: GET attr




######################
# EDIT CHILD PROFILE #
######################


@app.route('/child/edit<int:id>')
def edit_profile(id):
    """ Edit child profile """

    this_child = db.session.query(Child).filter_by(id=id).one()

    child_info = [ChildView(this_child)]

    return render_template('edit_profile.html', child_info=child_info)

#################
# ADD NEW CHILD #
#################

@app.route('/child/add', methods=['GET', 'POST'])
def add_profile():

    """add a child profile"""

    if request.method == 'POST':
        # get all new data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        guardian_type = request.form.get("guardian_type")
        guardian_fname = request.form.get("guardian_fname")
        guardian_lname = request.form.get("guardian_lname")
        medical_condition = request.form.get("medical_condition")
        doctor_appt = request.form.get("doctor_appt")
        situation = request.form.get("situation")
        home_visit = request.form.get("home_visit")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        
        if doctor_appt == "":
            doctor_appt = None

            print doctor_appt
            print type(doctor_appt)

        if home_visit == "":
            home_visit = None

        if medical_condition == "":
            medical_condition = None

        # print "Birth date: ", birth_date, " ", "Doct Appointment: ", doctor_appt, " ", "home visit: ", home_visit, " "
        # print type(home_visit)
        # print type(doctor_appt)
        # print type(birth_date)


        # seed into database
        child_entry = Child(first_name=first_name, last_name=last_name,
                            birth_date=birth_date, guardian_type=guardian_type, guardian_fname=guardian_fname,
                            guardian_lname=guardian_lname, medical_condition=medical_condition, doctor_appt=doctor_appt, situation=situation,
                            home_visit=home_visit, latitude=latitude, longitude=longitude)
        db.session.add(child_entry)
        db.session.commit()

        this_child = db.session.query(Child).order_by(Child.id.desc()).first()
        child_info = [ChildView(this_child)]

        return render_template('child_profile.html', child_info=child_info)
    else:
        return render_template('add_profile.html')


########
# MAIN #
########

if __name__ == '__main__':

    # debug = True as DebugToolbarExtension is invoked

    app.debug = True
    connect_to_db(app)

    # User the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
