""" Kid-O server"""

from jinja2 import StrictUndefined
from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)
from .models import db

app.config.from_object('app.settings')
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# Required to use Flask sessions and debug toolbar

app.secret_key = "ABC"

# Raise error if there is an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

from . import auth
from . import views
