""" Kid-O server"""

from jinja2 import StrictUndefined
from flask import Flask
from flask_seasurf import SeaSurf
from flask_static_compress import FlaskStaticCompress

app = Flask(__name__)
app.config.from_object('kido.settings.common')

csrf = SeaSurf(app)

from . import auth

compress = FlaskStaticCompress(app)

from .models import db

# Required to use Flask sessions and debug toolbar

app.secret_key = "ABC"

# Raise error if there is an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

from .admin import views as admin_views

from . import views
from . import api
