# -*- coding: utf-8 -*-


import re

from kido import app


NULL_PATTERN = re.compile(r'\0', re.U)


def allowed_file(filename):
    if "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def safe_unicode(s):
    """Removes invalid unicode characters from string.

    Invalid unicode characters in SQLAlchemy queries will cause exceptions, so
    this utility comes in handy in WTForms user input sanitization.
    """
    try:
        return str(s).encode("utf8", "surrogateescape").decode("utf8")
    except:
        return None


def remove_nulls(s):
    """Removes null characters from string.

    Null characters in SQLAlchemy queries will cause exceptions, so this
    utility comes in handy in WTForms user input sanitization.
    """
    try:
        return re.sub(NULL_PATTERN, '', s)
    except:
        return None
