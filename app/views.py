from app import app

from datetime import datetime, timedelta
import re
import os
import secrets
from sqlalchemy import or_, and_
from twilio import twiml
import urllib
from werkzeug import secure_filename

from flask import (
    render_template, 
    redirect, 
    request, 
    flash, 
    session, 
    url_for, 
    send_from_directory, 
    jsonify, 
    make_response, 
    abort,
)
from flask.ext.login import login_required, login_user, logout_user, current_user

from app.models import User, Child, db
from app import auth 
from app.child import ChildView
from app.forms import LoginForm, SignUpForm



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     """" Starting page with either login or personal profile if login session exists.
#     For Log in: take email, password from user and check if credentials exist in the database
#     by checking if email is in the users table. If email in table, redirect to the children overview.
#     If not: redirect to sign up page.
#     """
#     # if current_user.is_authenticated():
#     #     return redirect("/overview")
#     return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.

    form = LoginForm(request.form)
    next_url = request.args.get('next', '/overview')
    if request.method == 'POST' and form.validate(): # Process form if route gets POST request from /index
        next_url = request.form.get('next', '/overview')
        # credentials = (form.data['email'], form.data['password'])

        user = User.query.filter_by(email=form.data['email']).first()
        if user and user.password == form.data['password']:
            login_user(user)
            if not auth.is_safe_url(next_url):
                return abort(400)
            app.logger.info(next_url)
            return redirect(next_url or '/overview')

        if not user:
            flash('Please sign up!')
            return redirect('/signup')

        # Show error message ('Incorrect password.')
        form.errors["password"] = ["Incorrect password"]

    return render_template("login.html", form=form, next=next_url)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/signup', methods=['GET', 'POST'])
def signup_form():
    """ Sign up user """

    form = SignUpForm(request.form)
    next_url = request.form.get('next', '/overview')
    if request.method == 'POST' and form.validate():  # Process form if route gets POST request from /index
        next_url = request.form.get('next', '/overview')
        user_data = form.data
        del user_data['confirm']
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect('/overview')

    return render_template("signup.html", form=form, next=next_url)

@app.route('/overview', methods=['GET', 'POST'])
@login_required
def show_overview():
    """ Shows overview of all of the children in the project ordered by lastname."""

    if request.method == 'POST':  # Search function
        child_search = request.form.get('searchform')
        #  split string and if statement len 1, 2, 3 query.
        found_children = Child.query.filter(Child.fullname.ilike("%"+child_search+"%")).all()
        child_views = []

        for child in found_children:
            child_views.append(ChildView(child))

        if request.headers.get('Accept') == 'json':
            return jsonify(profiles=[x.to_dict() for x in child_views])

        return render_template('overview.html', child_profiles=child_views)

    else:
        all_children = Child.query.order_by(Child.last_name.asc()).all()
        child_views = []

        for child in all_children:
            child_views.append(ChildView(child))

        return render_template('overview.html', child_profiles=child_views)

@app.route('/child/<int:id>', methods=['GET', 'POST'])
@login_required
def child_profile(id):
    """ Show's each child's profile with the following information: First name, last name,
    age, birth date, guardian, siblings, medical condition, next doctor's appointment, sitution at
    home and school and when the next home visit is due. """

    if request.method == 'POST': # update child info from edit_profile.html form

        
        # Set pic_url to empty string to keep original path in case no changes are made.
        pic_url = ""
        file = request.files['file']
        # print "This should be the file: ", file
        if file and allowed_file(file.filename):
            # If no image is uploaded, this never passes.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the image path to send to the database
            pic_url = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)
        # get all new data
        # pic_url = request.form.get("file")
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

        if guardian_type == "":
            guardian_type = None

        if guardian_fname == "":
            guardian_fname = None

        if guardian_lname == "":
            guardian_lname = None

        if doctor_appt == "":
            doctor_appt = None

        if home_visit == "":
            home_visit = None

        if medical_condition == "":
            medical_condition = None

        if situation == "":
            situation = None


        # seed into database

        child_entry = db.session.query(Child).filter_by(id=id).one()
        if pic_url != "":
            child_entry.pic_url = pic_url
        # print "This should be a pic path: ", pic_url
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

@app.route('/child/edit<int:id>')
@login_required
def edit_profile(id):
    """ Edit child profile """

    this_child = db.session.query(Child).filter_by(id=id).one()

    child_info = [ChildView(this_child)]

    return render_template('edit_profile.html', child_info=child_info)

@app.route('/child/add', methods=['GET', 'POST'])
@login_required
def add_profile():

    """add a child profile"""

    if request.method == 'POST':
        # get all new data
        # Upload image 
        # import pdb; pdb.set_trace()
        file = request.files['file']
        print "This should be the file: ", file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the image path to send to the database
            imgroot = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)

        # Get all the other contents
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

        # Wordaround to avoid syntax errors for empty fields
        if doctor_appt == "":
            doctor_appt = None

        if home_visit == "":
            home_visit = None

        if medical_condition == "":
            medical_condition = None

        # if latitude is None:
        #     latitude = 18.542769

        # if longitude is None:
        #     longitude = -69.801216


        # seed into database
        child_entry = Child(pic_url=imgroot, first_name=first_name, last_name=last_name,
                            birth_date=birth_date, guardian_type=guardian_type, guardian_fname=guardian_fname,
                            guardian_lname=guardian_lname, medical_condition=medical_condition, doctor_appt=doctor_appt, situation=situation,
                            home_visit=home_visit, latitude=latitude, longitude=longitude)
        db.session.add(child_entry)
        db.session.commit()

        this_child = db.session.query(Child).order_by(Child.id.desc()).first()
        child_info = [ChildView(this_child)]
        child_id = this_child.id

        return redirect('/child/%d' % child_id)
    else:
        return render_template('add_profile.html')

def touch(path):
    # create empty file for image#
    with open(path, 'a'):
        os.utime(path, None)

@app.route('/twilio', methods=['GET', 'POST'])
def registerbysms():
    callers = secrets.callers
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    nummedia = request.values.get('NumMedia', None)
    mediaurl = request.values.get('MediaUrl0', None)
    message = "Hi! Please type in: REGISTER (First name of child) (Last name of Child) (Birth date (dd-mm-YYYY))"
    if from_number in callers:

        if body is not None:
            if body.find('REGISTER') != -1:
                child_info = body.split(" ")
                child_first_name = child_info[1]
                child_last_name = child_info[2]
                child_birth_date = child_info[3]
                date_check = re.match("([0-9]{2}-[0-9]{2}-[0-9]{4})", child_birth_date)
                if date_check is None:
                    message = "Hi " + callers[from_number] + "! " + "Can you please format the date correctly to: (mm)month-(dd)day-(YYYY)year?"
                else:
                    imgurl = '../static/images/childphotopreview.png'
                    if nummedia and mediaurl is not None:
                        imgurl = mediaurl

                    child_entry = Child(pic_url=imgurl, first_name=child_first_name, last_name=child_last_name, birth_date=child_birth_date, latitude=18.542769, longitude=-69.801216)

                    db.session.add(child_entry)
                    db.session.commit()
                    message = "Hi " + callers[from_number] + "! " + "Thank you for registering " + child_first_name + "! Please complete " + child_first_name + "'s profile on the Kid-O website."

    else:
        message = "Hello friend! If you want to use Kid-O please register on our website!"

    resp = twiml.Response()
    resp.message(message)
    return str(resp)

@app.route('/test')
def test():

    return render_template('test.html')
