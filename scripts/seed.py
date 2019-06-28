#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Utility file to seed children database from the list of our children's aid project in seed_data/"""

from flask_sqlalchemy import SQLAlchemy

from kido import app
from kido.models import Child, User, Project


def load_users():
    """ Load users from users.txt into database. """
    # import pdb; pdb.set_trace()
    fileinput = open("seed_data/users.txt")
    for line in fileinput.readlines():
        user_info = line.split("\t")
        user_entry = User(
            first_name=user_info[0],
            last_name=user_info[1],
            email=user_info[2],
            password=user_info[3],
        )

        db.session.add(user_entry)
        print(user_entry)
    db.session.commit()

    print("All users added to the database.")


def load_children():
    """ Load children from childrenslist.txt into database. """

    # with open("seed_data/childrenslist.txt") as fileinput:
    #     next(fileinput)

    fileinput = open("seed_data/childrenslist.txt")
    all_lines = fileinput.readlines()
    print("This is all lines:", all_lines)
    for line in all_lines:
        child_info = line.split("\t")
        print("The line is:", line)

        print("This is the child info:", child_info)
        child_entry = Child(
            photo=child_info[0],
            first_name=child_info[1],
            gender=child_info[2],
            last_name=child_info[3],
            nick_name=child_info[4],
            birth_date=child_info[5],
            birth_date_accuracy=child_info[6],
            nationality=child_info[7],
            guardian_type=child_info[8],
            guardian_fname=child_info[9],
            guardian_lname=child_info[10],
            number_of_siblings=child_info[11],
            siblings_in_project=child_info[12],
            school_name=child_info[13],
            school_class=child_info[14],
            school_attendance=child_info[15],
            projects=child_info[16],
            volonteer_task=child_info[17],
            situation=child_info[18],
            latitude=child_info[19],
            longitude=child_info[20],
        )
        db.session.add(child_entry)

        print(child_entry)
    db.session.commit()

    print("All children added to the database.")


def load_projects():
    fileinput = open("seed_data/projectslist.txt")
    all_lines = fileinput.readlines()
    for line in all_lines:
        project_info = line.split("\t")
        project_entry = Project(name=project_info[0].strip())

        db.session.add(project_entry)
    db.session.commit()

    print("All projects added.")


if __name__ == "__main__":
    db = SQLAlchemy(app)

    load_users()
    load_children()
    load_projects()
