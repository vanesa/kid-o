from app import app

from datetime import datetime, timedelta
import re
import os
try:
    import secrets
except ImportError:
    pass
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
    send_from_directory,
)
from flask.ext.login import login_required, login_user, logout_user, current_user

from app.models import User, Child, db
from app import auth 
from app import settings
from app.forms import LoginForm, SignUpForm, ChildForm


"""" Starting page with login.
For Log in: take email, password from user and check if credentials exist in the database
by checking if email is in the users table. If email in table, redirect to the children overview.
If not: redirect to sign up page.
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    """ Starting page with login.

    For Log in: take email, password from user and check if credentials exist in the database
    by checking if email is in the users table. If email in table, redirect to the children overview.
    If not: redirect to sign up page. WTForms validates the form. 
    """

    form = LoginForm(request.form)
    next_url = request.args.get('next', '/overview')
    if request.method == 'POST' and form.validate(): # Process form if route gets POST request from /index
        next_url = request.form.get('next', '/overview')
        user = User.query.filter_by(email=form.data['email']).first()
        if user and user.check_password(form.data['password']):
            login_user(user)
            if not auth.is_safe_url(next_url):
                return abort(400)
            app.logger.debug(next_url)
            return redirect(next_url or '/overview')

        if not user:
            return redirect('/signup')

        # Show error message ('Incorrect password.')
        form.errors["password"] = ["Incorrect password"]

    status_code = 400 if form.errors else 200
    return render_template("login.html", form=form, next=next_url), status_code

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

        if request.headers.get('Accept') == 'json':
            return jsonify(profiles=[x.to_dict() for x in found_children])

        return render_template('overview.html', child_profiles=found_children)

    else:
        all_children = Child.query.order_by(Child.last_name.asc()).all()

        return render_template('overview.html', child_profiles=all_children)

@app.route('/map')
@login_required
def load_map():
    all_children = Child.query.order_by(Child.last_name.asc()).all()
    return render_template('map.html', child_profiles=all_children)


@app.route('/child/<int:id>')
@login_required
def child_profile(id):
    """ Show's each child's profile with the following information: First name, last name,
    age, birth date, guardian, siblings, medical condition, next doctor's appointment, sitution at
    home and school and when the next home visit is due. """

    child = db.session.query(Child).filter_by(id=id).first()
    if child is None:
        abort(404)
    
    return render_template('child_profile.html', child=child)

@app.route('/child/edit<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """ Edit child profile """

    child = db.session.query(Child).filter_by(id=id).first()
    if child is None:
        abort(404)
    form = ChildForm(request.form)
    app.logger.debug(form.validate())
    app.logger.debug(form.errors)
    if request.method == 'POST' and form.validate():  # update child info from edit_profile.html form
        
        # Set pic_url to empty string to keep original path in case no changes are made.
        pic_url = ""
        file = request.files['file']
        # print "This should be the file: ", file
        if file and allowed_file(file.filename):
            # If no image is uploaded, this never passes.
            filename = secure_filename(file.filename)
            file.save(os.path.join("app/", app.config['UPLOAD_FOLDER'], filename))
            # Save the image path to send to the database
            pic_url = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)
        # get all new data
        # pic_url = request.form.get("file")

        app.logger.debug("inside this code")
        # seed into database
        if pic_url != "":
            child.pic_url = pic_url
        # print "This should be a pic path: ", pic_url
        child.first_name = form.data['first_name']
        child.last_name = form.data['last_name']
        child.birth_date = form.data['birth_date']
        child.guardian_type = form.data['guardian_type']
        child.guardian_fname = form.data['guardian_fname']
        child.guardian_lname = form.data['guardian_lname']
        child.medical_condition = form.data['medical_condition']
        child.doctor_appt = form.data['doctor_appt']
        child.situation = form.data['situation']
        child.home_visit = form.data['home_visit']
        child.latitude = form.data['latitude']
        child.longitude = form.data['longitude']

        db.session.commit()

        return redirect('/child/%d' % child.id)

    return render_template('edit_profile.html', form=form, child=child)

@app.route('/child/add', methods=['GET', 'POST'])
@login_required
def add_profile():

    """add a child profile"""
    form = ChildForm(request.form)
    app.logger.debug(form.validate())
    app.logger.debug(form.errors)
    if request.method == 'POST' and form.validate(): 
        # get all new data
        # Upload image 
        # import pdb; pdb.set_trace()
        file = request.files['file']
        imgroot = ''
        if file and allowed_file(file.filename):
            print "This should be the file: ", file
            filename = secure_filename(file.filename)
            file.save(os.path.join("app/", app.config['UPLOAD_FOLDER'], filename))
            # Save the image path to send to the database
            imgroot = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)

        # Get all the other contents
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        birth_date = form.data['birth_date']
        guardian_type = form.data['guardian_type']
        guardian_fname = form.data['guardian_fname']
        guardian_lname = form.data['guardian_lname']
        medical_condition = form.data['medical_condition']
        doctor_appt = form.data['doctor_appt']
        situation = form.data['situation']
        home_visit = form.data['home_visit']
        latitude = form.data['latitude']
        longitude = form.data['longitude']
        activity = True


        # seed into database
        child_entry = Child(pic_url=imgroot, first_name=first_name, last_name=last_name,
                            birth_date=birth_date, guardian_type=guardian_type, guardian_fname=guardian_fname,
                            guardian_lname=guardian_lname, medical_condition=medical_condition, doctor_appt=doctor_appt, situation=situation,
                            home_visit=home_visit, latitude=latitude, longitude=longitude, activity=activity)
        
        db.session.add(child_entry)
        db.session.commit()

        child = db.session.query(Child).order_by(Child.id.desc()).first()

        return redirect('/child/%d' % child.id)
    else:
        return render_template('add_profile.html', form=form)

@app.route('/delete-profile<int:id>', methods=['GET', 'POST'])
@login_required
def delete_profile(id):

    child = db.session.query(Child).filter_by(id=id).first()
    child_name = child.first_name + " " + child.last_name
    db.session.delete(child)
    db.session.commit()
    flash('You have deleted ' + child_name)
    return redirect('/overview')

def touch(path):
    # create empty file for image
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/x-icon')
