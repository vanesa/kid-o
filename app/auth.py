""" Authentification for Login """

from flask.ext.login import LoginManager
from app import app

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()
