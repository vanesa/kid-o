""" Kid-O server"""

from jinja2 import StrictUndefined
from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('app.settings')

from .models import db


# Required to use Flask sessions and debug toolbar

app.secret_key = "ABC"

# Raise error if there is an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

from . import auth
from . import views
