# -*- coding: utf-8 -*-
""" Kid-O server"""


__all__ = ["app", "admin", "models", "helpers", "views"]


from flask import Flask


app = Flask(__name__)
app.config.from_object("kido.settings.common")
app.secret_key = app.config["SECRET_KEY"]


import wtforms_json
from flask_seasurf import SeaSurf
from flask_static_compress import FlaskStaticCompress


csrf = SeaSurf(app)
compress = FlaskStaticCompress(app)
wtforms_json.init()


from . import admin, models, helpers, views
