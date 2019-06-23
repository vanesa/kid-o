# -*- coding: utf-8 -*-

import re
import io
import os
from datetime import datetime

try:
    import secrets
except ImportError:
    pass
from twilio.twiml.messaging_response import MessagingResponse

from flask import (
    abort,
    Blueprint,
    flash,
    jsonify,
    render_template,
    redirect,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_login import login_required

from PIL import Image

from kido import app, auth
from kido.models import (
    User,
    Child,
    Godparent,
    Project,
    ChildToGodparent,
    db,
    GodparentToProject,
)
from kido.constants import CHILD_HAS_GODPARENT, NO_NEED
from kido.forms import (
    LoginForm,
    SignUpForm,
    ChildForm,
    GodparentForm,
    SearchForm,
    GPSearchForm,
)
from kido.utils import allowed_file


blueprint = Blueprint("views", __name__)


@blueprint.route("/")
def index():
    if app.current_user.is_authenticated:
        return redirect(url_for('.overview'))
    return redirect(url_for('.login'))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next", request.form.get("next", "/overview"))
    if not auth.is_safe_url(next_url):
        next_url = "/overview"

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        if auth.login(form.data["email"], password=form.data["password"]):
            return redirect(next_url)
        else:
            flash("Invalid email or password.", category="error")

    status_code = 400 if form.errors else 200
    context = {"form": form, "next_url": next_url}
    return render_template("login.html", **context), status_code


@blueprint.route("/logout")
@login_required
def logout():
    auth.logout()
    return redirect(url_for('.login'))


@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    """ Sign up user """

    form = SignUpForm(request.form)
    next_url = request.form.get("next", "/overview")
    if (
        request.method == "POST" and form.validate()
    ):  # Process form if route gets POST request from /index
        next_url = request.form.get("next", "/overview")
        user_data = form.data
        del user_data["confirm"]
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        auth.login(user.email, force=True)

        return redirect(url_for('.overview'))

    return render_template("signup.html", form=form, next=next_url)


@blueprint.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    """ Shows overview of all of the children in the project ordered by lastname."""

    query = Child.query
    form = SearchForm(request.form)
    show_hidden_profiles = False
    flash_number_results = False

    if request.method == "POST" and form.validate():

        name = form.data.get("name")
        class_str = form.data.get("class_str")
        project = form.data.get("project")

        if name:
            query = query.filter(Child.fullname.ilike("%" + name + "%"))
            flash_number_results = True
        if class_str:
            query = query.filter(Child.school_class == class_str)
            flash_number_results = True
        if project:
            query = query.join(Child.projects).filter(Project.name == project)
            flash_number_results = True
        if form.data.get("show_hidden_profiles"):
            show_hidden_profiles = True

    if not show_hidden_profiles:
        query = query.filter(Child.is_active == True)
    children = query.order_by(Child.last_name.asc()).all()

    if flash_number_results and request.method == "POST":
        if len(children) == 0:
            flash("We could not find any child that matches your search. ")
        if len(children) > 1:
            flash("We found " + str(len(children)) + " profiles.")
        elif len(children) == 1:
            flash("We found 1 profile.")

    return render_template("overview.html", children=children, form=form)


@blueprint.route("/godparents-overview", methods=["GET", "POST"])
@login_required
def show_godparents_overview():
    """ Shows overview of all of the children in the project ordered by lastname."""

    query = Godparent.query
    form = GPSearchForm(request.form)
    flash_number_results = False

    if request.method == "POST" and form.validate():

        name = form.data.get("name")
        child_name = form.data.get("child_name")
        project = form.data.get("project")

        if name:
            query = query.filter(Godparent.gp_fullname.ilike("%" + name + "%"))
            flash_number_results = True
        if child_name:
            query = query.join(Godparent.children).filter(
                Child.fullname.ilike("%" + child_name + "%")
            )
            flash_number_results = True
        if project:
            query = query.join(Godparent.projects).filter(Project.name == project)
            flash_number_results = True

    godparents = query.order_by(Godparent.last_name.asc()).all()

    if flash_number_results and request.method == "POST":
        if len(godparents) == 0:
            flash("We could not find any child that matches your search. ")
        if len(godparents) > 1:
            flash("We found " + str(len(godparents)) + " profiles.")
        elif len(godparents) == 1:
            flash("We found 1 profile.")

    return render_template("godparents_overview.html", godparents=godparents, form=form)


@blueprint.route("/map")
@login_required
def load_map():
    form = SearchForm()
    all_children = Child.query.order_by(Child.last_name.asc()).all()
    return render_template("map.html", child_profiles=all_children, form=form)


@blueprint.route("/child/<string:child_id>")
@login_required
def child(child_id):
    child = db.session.query(Child).filter_by(id=child_id).first()
    if not child:
        abort(404)

    return render_template("child_profile.html", child=child)


@blueprint.route("/child/<string:child_id>/edit", methods=["GET", "POST"])
@login_required
def child_edit(child_id):
    child = Child.query.filter_by(id=child_id).first()
    if not child:
        abort(404)

    form = ChildForm(request.form, obj=child)
    form.projects.choices = [(p.name, p.name) for p in Project.query.all()]

    if (
        request.method == "POST" and form.validate()
    ):  # update child info from edit_profile.html form
        uploaded_photo = request.files["photo"]
        if uploaded_photo and allowed_file(uploaded_photo.filename):
            # resize proportional to baseheight
            baseheight = 250
            im = Image.open(uploaded_photo.stream)
            hpercent = baseheight / float(im.size[1])
            wsize = int((float(im.size[0]) * float(hpercent)))
            im = im.resize((wsize, baseheight), resample=Image.LANCZOS)
            image = io.BytesIO()
            im.save(image, format="JPEG")
            child.photo = image.getvalue()

        child.is_active = form.data["is_active"]
        child.gender = form.data["gender"]
        child.first_name = form.data["first_name"]
        child.last_name = form.data["last_name"]
        child.nick_name = form.data["nick_name"]
        child.birth_date = form.data["birth_date"]
        child.birth_date_accuracy = form.data["birth_date_accuracy"]
        child.nationality = form.data["nationality"]
        child.guardian_type = form.data["guardian_type"]
        child.guardian_fname = form.data["guardian_fname"]
        child.guardian_lname = form.data["guardian_lname"]
        child.number_of_siblings = form.data["number_of_siblings"]
        child.siblings_in_project = form.data["siblings_in_project"]
        child.school_class = form.data["school_class"]
        child.school_attendance = form.data["school_attendance"]
        child.volunteer_task = form.data["volunteer_task"]
        child.situation = form.data["situation"]
        child.godparent_status = form.data["godparent_status"]
        child.latitude = form.data["latitude"]
        child.longitude = form.data["longitude"]

        # add child projects if necessary
        projects = child.projects.all()
        for proj in form.data.get("projects"):
            proj = Project.query.filter_by(name=proj).first()
            if proj not in projects:
                projects.append(proj)

        # remove child projects
        for proj in projects:
            if proj.name not in form.data.get("projects"):
                projects = list(filter(lambda p: p.name != proj.name, projects))

        child.projects = projects

        # when hiding a child, turn existing godparent into project godparent
        if child.is_active == False and child.godparents:
            for g in child.godparents:
                remove_godparent(g.id)
                data = {}
                # data['project_id'] = orphanage.id
                data["godparent_id"] = g.id
                sponsorship = GodparentToProject(**data)
                db.session.add(sponsorship)
                child.godparent_status = NO_NEED

        # if no godparent is added, remove godparent status
        if child.godparent_status == CHILD_HAS_GODPARENT and not child.godparents.all():
            child.godparent_status = None

        db.session.commit()

        return redirect(url_for(".child", child_id=child.id))

    # TODO: display these errors in the template and delete this line
    if form.errors:
        app.logger.debug(form.errors)

    context = {
        "form": form,
        "child": child,
        "godparents_available": [
            {"id": g.id, "name": str(g), "selected": g in child.godparents}
            for g in Godparent.query.all()
        ],
    }
    return render_template("edit_profile.html", **context)


@blueprint.route("/child/add", methods=["GET", "POST"])
@login_required
def add_profile():

    """ Add a child profile """
    form = ChildForm(request.form)
    form.projects.choices = [(p.name, p.name) for p in Project.query.all()]

    if request.method == "POST" and form.validate():
        data = form.data

        uploaded_photo = request.files["photo"]
        if uploaded_photo and allowed_file(uploaded_photo.filename):
            # resize proportional to baseheight
            baseheight = 250
            im = Image.open(uploaded_photo.stream)
            hpercent = baseheight / float(im.size[1])
            wsize = int((float(im.size[0]) * float(hpercent)))
            im = im.resize((wsize, baseheight), resample=Image.LANCZOS)
            image = io.BytesIO()
            im.save(image, format="JPEG")
            data["photo"] = image.getvalue()
        else:
            data["photo"] = None

        # seed into database
        data["projects"] = [
            Project.query.filter_by(name=x).first() for x in data["projects"]
        ]
        child = Child(**data)

        db.session.add(child)
        db.session.commit()
        return redirect(url_for(".child", child_id=child.id))

    app.logger.debug(form.errors)
    projects = [(p.name) for p in Project.query.all()]
    return render_template("add_profile.html", form=form, projects=projects)


@blueprint.route("/delete-profile/<string:id>", methods=["POST"])
@login_required
def delete_profile(id):

    child = db.session.query(Child).filter_by(id=id).first()
    child_name = child.first_name + " " + child.last_name
    db.session.delete(child)
    db.session.commit()
    flash("You have deleted " + child_name + "'s profile.")
    return redirect(url_for(".overview"))


@blueprint.route("/create-godparent", methods=["POST"])
@login_required
def create_godparent():
    """create a godparent profile"""

    form = GodparentForm.from_json(request.get_json())
    if form.validate():

        # seed into database
        godparent = Godparent(**form.data)
        db.session.add(godparent)
        db.session.commit()
        return jsonify(success=True), 201


@blueprint.route("/add-godparent/<string:child_id>", methods=["POST"])
@login_required
def add_godparent(child_id):
    """add a godparent profile"""

    child = Child.query.filter_by(id=child_id).first()
    if not child:
        abort(404)

    form = GodparentForm.from_json(request.get_json())
    if form.validate():

        # seed into database
        godparent = Godparent(**form.data)
        db.session.add(godparent)
        child.godparents.append(godparent)
        db.session.commit()
        return jsonify(success=True), 201

    app.logger.debug(form.errors)
    return jsonify(errors=form.errors), 400


@blueprint.route("/add-existing-godparent/<string:child_id>", methods=["POST"])
@login_required
def add_existing_godparent(child_id):
    """add a godparent profile"""

    child = Child.query.filter_by(id=child_id).first()
    if not child:
        abort(404)

    data = request.get_json()

    if data.get("ids"):
        for g in data["ids"]:
            godparent = Godparent.query.filter_by(id=g).first()
            child.godparents.append(godparent)
        child.godparent_status = CHILD_HAS_GODPARENT
        db.session.commit()
    return jsonify(success=True), 201


@blueprint.route("/remove-godparent/<string:id>", methods=["POST"])
@login_required
def remove_godparent(id):
    godparent = Godparent.query.filter_by(id=id).first()
    godparent.is_active = False
    child_to_gp = ChildToGodparent.query.filter_by(godparent_id=id).first()
    child = Child.query.filter_by(id=child_to_gp.child_id).first()
    app.logger.debug(child_to_gp)
    old_history = godparent.sponsorship_history

    if old_history:
        godparent.sponsorship_history = (
            old_history
            + godparent.first_name
            + " "
            + godparent.last_name
            + " sponsored "
            + child.first_name
            + " "
            + child.last_name
            + " from "
            + str(child_to_gp.created_at)
            + " until "
            + str(datetime.now())
            + "\n"
        )
    else:
        godparent.sponsorship_history = (
            godparent.first_name
            + " "
            + godparent.last_name
            + " sponsored "
            + child.first_name
            + " "
            + child.last_name
            + " from "
            + str(child_to_gp.created_at)
            + " until "
            + str(datetime.now())
            + "\n"
        )

    ChildToGodparent.query.filter_by(godparent_id=id).delete()

    if not child.godparents.all():
        child.godparent_status = NO_NEED
    godparent_name = godparent.first_name + " " + godparent.last_name

    db.session.commit()

    flash(
        "You have removed "
        + godparent_name
        + " as a godparent to "
        + child.first_name
        + "."
    )
    return jsonify(success=True)


@blueprint.route("/twilio", methods=["GET", "POST"])
def registerbysms():
    callers = secrets.callers
    from_number = request.values.get("From", None)
    body = request.values.get("Body", None)
    nummedia = request.values.get("NumMedia", None)
    mediaurl = request.values.get("MediaUrl0", None)
    message = "Hi! Please type in: REGISTER (First name of child) (Last name of Child) (Birth date (mm-dd-YYYY))"
    if from_number in callers:

        if body is not None:
            if body.find("REGISTER") != -1:
                child_info = body.split(" ")
                child_first_name = child_info[1]
                child_last_name = child_info[2]
                child_birth_date = child_info[3]
                date_check = re.match("([0-9]{2}-[0-9]{2}-[0-9]{4})", child_birth_date)
                if date_check is None:
                    message = (
                        "Hi "
                        + callers[from_number]
                        + "! "
                        + "Can you please format the date correctly to: (mm)month-(dd)day-(YYYY)year?"
                    )
                else:
                    imgurl = "../static/images/childphotopreview.png"
                    if nummedia and mediaurl is not None:
                        imgurl = mediaurl

                    child_entry = Child(
                        photo_url=imgurl,
                        first_name=child_first_name,
                        last_name=child_last_name,
                        birth_date=child_birth_date,
                    )

                    db.session.add(child_entry)
                    db.session.commit()
                    message = (
                        "Hi "
                        + callers[from_number]
                        + "! "
                        + "Thank you for registering "
                        + child_first_name
                        + "! Please complete "
                        + child_first_name
                        + "'s profile on the Kid-O website."
                    )
            else:
                message = (
                    "Hi "
                    + callers[from_number]
                    + "! Please type in: REGISTER (First name of child) (Last name of child) (Birth date (mm-dd-YYYY))"
                )
    else:
        message = (
            "Hello friend! If you want to use Kid-O please register on our website!"
        )

    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


@blueprint.route("/child_photo/<string:child_id>", methods=["GET"])
def child_photo(child_id):
    child = Child.query.filter_by(id=child_id).first()
    if not child:
        abort(404)

    return send_file(
        io.BytesIO(child.photo),
        attachment_filename="{0}.jpg".format(child.id),
        mimetype="image/jpg",
    )


@blueprint.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static", "images"),
        "favicon.ico",
        mimetype="image/x-icon",
    )


app.register_blueprint(blueprint)
