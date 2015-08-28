""" Utility file to seed children database from the list of our children's aid project in seed_data/"""

from app.models import Child, User, connect_to_db, db
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
        child_entry = Child(pic_url=child_info[0], first_name=child_info[1], last_name=child_info[2],
                            birth_date=child_info[3], guardian_type=child_info[4], guardian_fname=child_info[5],
                            guardian_lname=child_info[6], medical_condition=child_info[7], doctor_appt=child_info[8], situation=child_info[9],
                            home_visit=child_info[10], latitude=child_info[11], longitude=child_info[12])
        db.session.add(child_entry)
       
        print child_entry
    db.session.commit()

    print "All children added to the database."

##################

if __name__ == "__main__":
    connect_to_db(app)

    load_children()
    load_users()
