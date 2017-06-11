from app import app

from datetime import datetime, timedelta
import re
import os
try:
    import secrets
except ImportError:
    pass
from sqlalchemy import or_, and_
import urllib
from werkzeug import secure_filename

from flask import (
    request,
    session, 
    url_for, 
    send_from_directory, 
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