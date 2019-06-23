# -*- coding: utf-8 -*-

__all__ = ["login", "logout", "login_required", "is_uuid4", "is_safe_url"]


from flask_login import login_required, LoginManager, current_user

from kido import app
from kido.models import User


app.current_user = current_user


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "views.login"


from .helpers import login, logout, is_uuid4, is_safe_url


@login_manager.user_loader
def load_user(userid):
    if not is_uuid4(userid):
        return None
    return User.query.filter_by(id=userid).first()
