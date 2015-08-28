#!/usr/bin/env python

from flask_debugtoolbar import DebugToolbarExtension

from app import app
from app.models import connect_to_db


if __name__ == '__main__':

    # debug = True as DebugToolbarExtension is invoked

    app.debug = False
    connect_to_db(app)

    # User the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
