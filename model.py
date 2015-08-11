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

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s password=%s>" % (self.id, self.first_name, self.last_name, self.email, self.password)


class Child(db.Model):
    """Child of Kid-O App."""

    __tablename__= "children"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pic_url = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    guardian_type = db.Column(db.String(50), nullable=True)
    guardian_fname = db.Column(db.String(32), nullable=True)
    guardian_lname = db.Column(db.String(32), nullable=True)
    doctor_appt = db.Column(db.DateTime, nullable=True)
    situation = db.Column(db.Text, nullable=True)
    home_visit = db.Column(db.DateTime, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Child id=%s first_name=%s last_name=%s>" % (self.id, self.first_name, self.last_name)

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
