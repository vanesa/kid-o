""" Utility file to seed children database from the list of our children's aid project in seed_data/"""

from flask_sqlalchemy import SQLAlchemy
from app.models import Child, User, Project
from app import app


def load_users(db):
    """ Load users from users.txt into database. """
    with open("seed_data/users.txt", 'r') as finput:
        for line in finput.readlines():
            user_info = line.split("\t")
            user_entry = User(first_name=user_info[0], last_name=user_info[1], email=user_info[2],
                              password=user_info[3])
            db.session.add(user_entry)
            print user_entry
    db.session.commit()

    print "All users added to the database."


def load_children(db):
    """ Load children from childrenslist.txt into database. """
    with open("seed_data/childrenslist.txt", 'r') as finput:
        all_lines = finput.readlines()
        print "This is all lines:", all_lines
        for line in all_lines:
            child_info = line.split("\t")
            print "The line is:", line
            print "This is the child info:", child_info
            child_entry = Child(photo=child_info[0], first_name=child_info[1], gender=child_info[2],
                                last_name=child_info[3], nick_name="",
                                birth_date=child_info[4], birth_date_accuracy=child_info[5], nationality=child_info[6],
                                guardian_type=child_info[7], guardian_fname=child_info[8],
                                guardian_lname=child_info[9], number_of_siblings=child_info[10],
                                siblings_in_project=child_info[11], school_name=child_info[12],
                                school_class="",
                                school_attendance=child_info[13], projects=set(),
                                volunteer_task="",
                                situation=child_info[14], latitude=child_info[15], longitude=child_info[16])
            db.session.add(child_entry)
            print child_entry
    db.session.commit()
    print "All children added to the database."


def load_projects(db):
    with open("seed_data/projectslist.txt", 'r') as finput:
        all_lines = finput.readlines()
        for line in all_lines:
            project_info = line.split("\t")
            project_entry = Project(name=project_info[0].strip())
            db.session.add(project_entry)
        db.session.commit()
    print "All projects added."


def main():
    db = SQLAlchemy(app)
    load_users(db)
    load_children(db)
    load_projects(db)


if __name__ == "__main__":
    main()
