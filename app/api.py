from app import app

from datetime import datetime, timedelta
import re
import os
from sqlalchemy import or_, and_

from flask import (
    request,
    jsonify, 
)
from flask_login import login_required, login_user, logout_user, current_user

from app.models import User, Child, Godparent, db
from app import auth 
from app import settings


@app.route('/api/children_profiles', methods=['GET'])
def getChildrenProfiles():

    """ Gets all of the children profiles in the project. """
    query = Child.query
    
    children = query.order_by(Child.last_name.asc()).all()

    return jsonify(profiles=[x.to_dict() for x in children])

@app.route('/api/child_profile/<string:id>', methods=['GET'])
def getChildProfile(id):

    """ Gets all of the children profiles in the project. """
    child = db.session.query(Child).filter_by(id=id).first()

    if child is None:
        abort(404)

    return jsonify(profile=[child.to_dict()])
