#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from kido import app
from kido.constants import PERMISSION_ADMIN
from kido.forms import EmailForm
from kido.models import db, User, Group, Permission


def main():

    if not len(sys.argv) == 2:
        print("Missing email.")
        return -1

    with app.app_context():
        form = EmailForm.from_json({"email": sys.argv[1]})
        if not form.validate():
            print("Error: {}".format(form.errors["email"][0]))
            return -2

    email = form.data["email"]

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(first_name="Admin", email=email, password="123456789")
        db.session.add(user)
        db.session.commit()

    group = Group.query.filter_by(name="Admin").first()
    if group is None:
        group = Group(name="Admin")
        group.permissions.append(Permission(name=PERMISSION_ADMIN))
        db.session.add(group)
        db.session.commit()

    user.groups.append(group)
    db.session.commit()

    print("Added user as admin. They can now access the /admin url.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
