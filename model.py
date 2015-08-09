"""Models and database functions for Kid-O project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

########


######################
# Model definitions #
#####################


class User(db.Model):
    """User of Kid-O App."""

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_first_name = db.Column(db.String(32), nullable=False)
    user_last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s user_first_name=%s user_last_name=%s email=%s password=%s>" % (self.user_id, self.user_first_name, self.user_last_name, self.email, self.password)


class Child(db.Model):
    """Child of Kid-O App."""

    __tablename__= "children"

    child_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    child_pic_url = db.Column(db.String, nullable=True)
    child_first_name = db.Column(db.String(32), nullable=False)
    child_last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    caregiver_type = db.Column(db.String(50), nullable=True)
    caregiver_first_name = db.Column(db.String(32), nullable=True)
    caregiver_last_name = db.Column(db.String(32), nullable=True)
    doctor_appt = db.Column(db.DateTime, nullable=True)
    situation = db.Column(db.Text, nullable=True)
    home_visit = db.Column(db.DateTime, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Child child_id=%s child_first_name=%s child_last_name=%s>" % (self.child_id, self.child_first_name, self.child_last_name)

    # Add here a model to calculate age?

#####################
# Helper functions #
###################

def connect_to_db(app):
    """Connect the database to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/kid-o'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
