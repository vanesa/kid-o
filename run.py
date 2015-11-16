#!/usr/bin/env python

from flask_debugtoolbar import DebugToolbarExtension

from app import app
from app.models import connect_to_db
import os


if __name__ == '__main__':

    # debug = True as DebugToolbarExtension is invoked

    connect_to_db(app)

    # User the DebugToolbar
    # DebugToolbarExtension(app)
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=PORT)
	# debug = False if os.environ.get()