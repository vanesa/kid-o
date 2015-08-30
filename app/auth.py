""" Authentification for Login """

from flask import request
from flask.ext.login import LoginManager
from app import app
from app.models import User
from urlparse import urlparse, urljoin

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc