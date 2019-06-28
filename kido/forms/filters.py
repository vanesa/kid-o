# -*- coding: utf-8 -*-


from email_validator import validate_email, EmailNotValidError

from kido.utils import safe_unicode, remove_nulls


def lower(data):
    return data.lower() if data else data


def strip(data):
    try:
        return safe_unicode(remove_nulls(data)).strip()
    except:
        return None


def email(data):
    data = strip(data)
    if not data:
        return data
    else:
        try:
            return validate_email(data, check_deliverability=False)['email']
        except EmailNotValidError:
            return data
