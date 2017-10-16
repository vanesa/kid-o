""" Authentification for Login """

import re
from flask import request
from flask_login import LoginManager
from app import app
from app.models import User
from urlparse import urlparse, urljoin

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    if not is_uuid4(userid):
        return None
    return User.query.filter_by(id=userid).first()


def is_uuid4(text):
    if text:
        try:
            return not not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', text, re.I)
        except:
            pass
    return False


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
