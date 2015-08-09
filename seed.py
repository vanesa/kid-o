""" Utility file to seed children database from the list of our children's aid project in seed_data/"""

from model import Child, User, connect_to_db, db
from server import app
from datetime import datetime

def load_users():
    """ Load users from users.txt into database. """
    # import pdb; pdb.set_trace()
    fileinput = open("seed_data/users.txt")
    for line in fileinput.readlines():
        user_info = line.split("\t")
        user_entry = User(user_first_name=user_info[0], user_last_name=user_info[1], email=user_info[2], 
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
    for line in fileinput.readlines():
        child_info = line.split("\t")
        child_entry = Child(child_pic_url=child_info[0], child_first_name=child_info[1], child_last_name=child_info[2],
                            birth_date=child_info[3], caregiver_type=child_info[4], caregiver_first_name=child_info[5],
                            caregiver_last_name=child_info[6], doctor_appt=child_info[7], situation=child_info[8],
                            home_visit=child_info[9], latitude=child_info[10], longitude=child_info[11])
        db.session.add(child_entry)
        # import pdb; pdb.set_trace()
        print child_entry
    db.session.commit()

    print "All children added to the database."

##################

if __name__ == "__main__":
    connect_to_db(app)

    load_children()
    load_users()
