""" Utility file to seed children database from the list of our children's aid project in seed_data/"""

from flask_sqlalchemy import SQLAlchemy
from app.models import Child, User, Project
from app import app
from datetime import datetime

def load_users():
    """ Load users from users.txt into database. """
    # import pdb; pdb.set_trace()
    fileinput = open("seed_data/users.txt")
    for line in fileinput.readlines():
        user_info = line.split("\t")
        user_entry = User(first_name=user_info[0], last_name=user_info[1], email=user_info[2], 
            password=user_info[3])

        db.session.add(user_entry)
        print user_entry
    db.session.commit()

    print "All users added to the database."


def load_children():
    """ Load children from childrenslist.txt into database. """

    # with open("seed_data/childrenslist.txt") as fileinput:
    #     next(fileinput)

    fileinput = open("seed_data/childrenslist.txt")
    all_lines = fileinput.readlines()
    print "This is all lines:", all_lines
    for line in all_lines:
        child_info = line.split("\t")
        print "The line is:", line
        
        print "This is the child info:", child_info
        child_entry = Child(photo_url=child_info[0], first_name=child_info[1], last_name=child_info[2],
                            birth_date=child_info[3], nationality=child_info[4], guardian_type=child_info[5], guardian_fname=child_info[6],
                            guardian_lname=child_info[7], number_of_siblings=child_info[8], siblings_in_project=child_info[9], school_class=child_info[10], 
                            school_attendance=child_info[11], situation=child_info[12], latitude=child_info[13], longitude=child_info[14])
        db.session.add(child_entry)
       
        print child_entry
    db.session.commit()

    print "All children added to the database."

def load_projects():
    fileinput = open("seed_data/projectslist.txt")
    all_lines = fileinput.readlines()
    for line in all_lines:
        project_info = line.split("\t")
        project_entry = Project(name=project_info[0].strip())

        db.session.add(project_entry)
    db.session.commit()

    print "All projects added."


##################

if __name__ == "__main__":
    db = SQLAlchemy(app)

    load_users()
    load_children()
    load_projects()
