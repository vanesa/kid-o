# -*- coding: utf-8 -*-

import re
from datetime import datetime
from flask import request
from flask_login import login_user, logout_user
from urllib import parse as urlparse

from kido import app
from kido.models import db, User


def login(email, password=None, remember=True, force=False):
    user = User.query.filter_by(email=email).first()
    if user:
        if (
            not force
            and user.failed_login_count >= app.config["MAX_FAILED_LOGIN_ATTEMPTS"]
        ):
            return False
        if force or user.check_password(password):
            if login_user(user, remember=remember):
                user.last_login_at = datetime.utcnow()
                user.failed_login_count = 0
                db.session.commit()
                return True
        else:
            user.failed_login_count += 1
            db.session.commit()
    return False


def logout():
    return logout_user()


def is_uuid4(text):
    if text:
        try:
            return not not re.match(
                r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$",
                text,
                re.I,
            )
        except:
            pass
    return False


def is_safe_url(target):
    ref_url = urlparse.urlparse(request.host_url)
    test_url = urlparse.urlparse(urlparse.urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
