#!/usr/bin/env python

import sys

from kido.constants import PERMISSION_ADMIN
from kido.models import db, User, Group, Permission


def main():

    if not len(sys.argv) == 2:
        return "Missing email"

    user = User.query.filter_by(email=sys.argv[1]).first()
    if user is None:
        return "User not found"

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
