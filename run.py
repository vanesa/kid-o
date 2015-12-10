#!/usr/bin/env python

from flask_debugtoolbar import DebugToolbarExtension

from app import app
import os


if __name__ == '__main__':

    # debug = True as DebugToolbarExtension is invoked

    # User the DebugToolbar
    # DebugToolbarExtension(app)
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=PORT)
	# debug = False if os.environ.get()