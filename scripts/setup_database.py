#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from alembic import command
from alembic.config import Config
from subprocess import call

from kido import app
from kido.models import db


def main():
    prompt = "Really drop and recreate {dbname} database? (y/N)".format(
        dbname=app.config["DB_NAME"]
    )

    force = True if len(sys.argv) > 1 and sys.argv[1] == "--force" else False
    if force or input(prompt) == "y":
        if not os.path.exists("alembic/versions"):
            os.mkdir("alembic/versions")

        statements = [
            "DROP DATABASE IF EXISTS {}".format(app.config["DB_NAME"]),
            "CREATE USER {u} WITH ENCRYPTED PASSWORD '{p}'".format(
                u=app.config["DB_USERNAME"], p=app.config["DB_PASSWORD"]
            ),
            "CREATE DATABASE {dbname} WITH OWNER {u}".format(
                dbname=app.config["DB_NAME"], u=app.config["DB_USERNAME"]
            ),
        ]
        for st in statements:
            call(["psql", "-c", st])

        db.create_all()
        print("Created all tables.")
        alembic_cfg = Config("alembic.ini")
        command.stamp(alembic_cfg, "head")
        print("Configured alembic.")
    else:
        print("Exiting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
