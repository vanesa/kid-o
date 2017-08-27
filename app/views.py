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
from flask_login import login_required, login_user, logout_user, current_user

from PIL import Image

from app.models import User, Child, Godparent, db
from app import auth 
from app import settings
from app.forms import LoginForm, SignUpForm, ChildForm, GodparentForm, SearchForm


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
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/signup', methods=['GET', 'POST'])
def signup_form():
    """ Sign up user """

    form = SignUpForm(request.form)
    next_url = request.form.get('next', '/overview')
    if request.method == 'POST' and form.validate():  # Process form if route gets POST request from /index
        next_url = request.form.get('next', '/overview')
        user_data = form.data
        app.logger.debug(user_data)
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

    query = Child.query
    form = SearchForm(request.form)
    show_hidden_profiles = False
    flash_number_results = False
    
    if request.method == 'POST' and form.validate():

        name = form.data.get('name')
        class_str = form.data.get('class_str')

        if name:
            query = query.filter(Child.fullname.ilike("%"+name+"%"))
            flash_number_results = True
        if class_str:
            query = query.filter(Child.school_class == class_str)
            flash_number_results = True
        if form.data.get('show_hidden_profiles'):
            show_hidden_profiles = True

        # if request.headers.get('Accept') == 'json':
        #     return jsonify(profiles=[x.to_dict() for x in children])

    if not show_hidden_profiles:
        query = query.filter(Child.is_active==True)
    children = query.order_by(Child.last_name.asc()).all()

    if flash_number_results and request.method == 'POST':
        if len(children) == 0:
            flash('We could not find any child that matches your search. ')
        if len(children) > 1:
            flash('We found ' + str(len(children)) + ' profiles.')
        elif len(children) == 1:
            flash('We found 1 profile.')
    
    return render_template('overview.html', children=children, form=form)

@app.route('/map')
@login_required
def load_map():
    form = SearchForm()
    all_children = Child.query.order_by(Child.last_name.asc()).all()
    return render_template('map.html', child_profiles=all_children, form=form)


@app.route('/child/<string:id>')
@login_required
def child_profile(id):
    """ Show's each child's profile """

    child = db.session.query(Child).filter_by(id=id).first()
    if child is None:
        abort(404)
    
    return render_template('child_profile.html', child=child)

@app.route('/child/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """ Edit child profile """

    child = db.session.query(Child).filter_by(id=id).first()
    # godparent = db.session.query(Godparent).filter_by(id=child_id).first()

    if child is None:
        abort(404)
    form = ChildForm(request.form, obj=child)
    if request.method == 'POST' and form.validate():  # update child info from edit_profile.html form
        # Set photo_url to empty string to keep original path in case no changes are made.
        app.logger.debug(form.validate())
        photo_url = ""
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            # If no image is uploaded, this never passes.
            child_name = form.data['first_name'].lower() + form.data['last_name'].lower()
            photo_format = photo.filename.split('.')[1].lower()
            filename = secure_filename(child_name + '.' + photo_format)
            
            # resize proportional to baseheight            
            baseheight = 250
            im = Image.open(photo.stream)
            hpercent = (baseheight/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize, baseheight), resample=Image.LANCZOS)
            path = os.path.abspath(os.path.join("app/", app.config['UPLOAD_FOLDER'], filename))
            im.save(path)

            # Save the image path to send to the database
            photo_url = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)
        # get all new data

        # seed into database
        if photo_url != "":
            child.photo_url = photo_url
        # seed into database
        child.is_active= form.data['is_active']
        child.first_name = form.data['first_name']
        child.last_name = form.data['last_name']
        child.nick_name = form.data['nick_name']
        child.birth_date = form.data['birth_date']
        child.nationality = form.data['nationality']
        child.guardian_type = form.data['guardian_type']
        child.guardian_fname = form.data['guardian_fname']
        child.guardian_lname = form.data['guardian_lname']
        child.number_of_siblings = form.data['number_of_siblings']
        child.siblings_in_project = form.data['siblings_in_project']
        child.school_class = form.data['school_class']
        child.school_attendance = form.data['school_attendance']
        child.volunteer_task = form.data['volunteer_task']
        child.situation = form.data['situation']
        child.godparent_status = form.data['godparent_status']
        child.latitude = form.data['latitude']
        child.longitude = form.data['longitude']

        db.session.commit()

        return redirect('/child/%s' % child.id)

    app.logger.debug(form.errors)
    app.logger.debug("latitude: ", child.latitude)

    return render_template('edit_profile.html', form=form, child=child)

@app.route('/child/add', methods=['GET', 'POST'])
@login_required
def add_profile():

    """ Add a child profile """
    form = ChildForm(request.form)

    if request.method == 'POST' and form.validate(): 
        # Upload image 
        photo = request.files['photo']
        photo_url = ''

        if photo and allowed_file(photo.filename):

            print "This should be the file: ", photo
            child_name = (form.data['first_name'] + form.data['last_name']).lower()
            photo_format = photo.filename.split('.')[1].lower()
            filename = secure_filename(child_name + '.' + photo_format)

            # resize proportional to baseheight 
            baseheight = 250
            im = Image.open(photo.stream)
            hpercent = (baseheight/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize, baseheight), resample=Image.LANCZOS)

            path = os.path.abspath(os.path.join("app/", app.config['UPLOAD_FOLDER'], filename))
            im.save(path)

            # Save the image path to send to the database
            photo_url = os.path.join("/", app.config['UPLOAD_FOLDER'], filename)

        # seed into database
        data = form.data
        data['photo_url'] = photo_url
        child = Child(**data)
        
        db.session.add(child)
        db.session.commit()
        return redirect('/child/%s' % child.id)
    
    app.logger.debug(form.errors)
    return render_template('add_profile.html', form=form)

@app.route('/delete-profile/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_profile(id):

    child = db.session.query(Child).filter_by(id=id).first()
    child_name = child.first_name + " " + child.last_name
    filename = child.first_name + child.last_name + ".jpg"
    try:
        os.remove(os.path.join("app/", app.config['UPLOAD_FOLDER'], filename))
    except:
        pass
    db.session.delete(child)
    db.session.commit()
    flash('You have deleted ' + child_name + "'s profile.")
    return redirect('/overview')

@app.route('/add-godparent/<string:child_id>', methods=['POST'])
@login_required
def add_godparent(child_id):
    """add a godparent profile"""
    
    child = Child.query.filter_by(id=child_id).first()
    if not child:
        abort(404)

    form = GodparentForm(obj=request.get_json())
    if form.validate():

        # seed into database
        godparent = Godparent(**form.data)
        db.session.add(godparent)
        child.godparents.append(godparent)
        db.session.commit()
        return '{"success": true}'
    
    app.logger.debug(form.errors)
    return '{"error": true}', 400

@app.route('/delete-godparent/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_godparent(id):

    godparent = db.session.query(Godparent).filter_by(id=id).first()
    godparent_name = godparent.first_name + " " + godparent.last_name
    db.session.delete(godparent)
    db.session.commit()
    flash('You have deleted ' + godparent_name + ".")
    return '{"success": true}'

@app.route('/twilio', methods=['GET', 'POST'])
def registerbysms():
    callers = secrets.callers
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    nummedia = request.values.get('NumMedia', None)
    mediaurl = request.values.get('MediaUrl0', None)
    message = "Hi! Please type in: REGISTER (First name of child) (Last name of Child) (Birth date (mm-dd-YYYY))"
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
                message = "Hi " + callers[from_number] + "! Please type in: REGISTER (First name of child) (Last name of child) (Birth date (mm-dd-YYYY))"
    else:
        message = "Hello friend! If you want to use Kid-O please register on our website!"

    resp = twiml.Response()
    resp.message(message)
    return str(resp)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/x-icon')
