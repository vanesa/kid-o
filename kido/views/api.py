# -*- coding: utf-8 -*-

from flask import abort, Blueprint, jsonify

from kido import app
from kido.models import db, Child


blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint, url_prefix='/api')


@blueprint.route('/children_profiles', methods=['GET'])
def getChildrenProfiles():
    """ Gets all of the children profiles in the project. """
    query = Child.query

    children = query.order_by(Child.last_name.asc()).all()

    return jsonify(profiles=[x.to_dict() for x in children])


@blueprint.route('/child_profile/<string:id>', methods=['GET'])
def getChildProfile(id):
    """ Gets a Child's profile in the project. """
    child = db.session.query(Child).filter_by(id=id).first()

    if child is None:
        abort(404)

    return jsonify(profile=[child.to_dict()])


@blueprint.route('/children_location', methods=['GET'])
def getChildrenHomeLocation():
    """ Gets all of the active children home locations in the project. """
    query = Child.query
    query = query.filter(Child.latitude != None)
    query = query.filter(Child.is_active)

    children_with_location = query.order_by(Child.last_name.asc()).all()

    return jsonify(profiles=[x.to_dict() for x in children_with_location])


app.register_blueprint(blueprint)
