import os
import unittest
import tempfile
import json

from app import app, csrf
from app.models import db, Child, User
from datetime import datetime

class ChildViewTestCase(unittest.TestCase):
    
    def test_child_view(self):
        first_name = "Martha"
        last_name = "Sosa"
        birth_date= datetime.strptime("2009-02-02", "%Y-%m-%d")

        test_child_view = Child(first_name=first_name, last_name=last_name, birth_date=birth_date)

        currenttime = datetime.now()
        expected_age = (currenttime - birth_date).days / 365
        self.assertEqual(test_child_view.age, expected_age)

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_can_login(self):
        password = "testpass"
        user = User(
            first_name="Testuser",
            last_name="Tester",
            email="test@tester.com",
            password=password,
        )
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/', data=dict(
            email=user.email,
            password=password,
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Log Out", response.get_data())

        db.session.delete(user)
        db.session.commit()

    def test_can_sign_out(self):
        password = "testpass"
        user = User(
            first_name="Testuser",
            last_name="Tester",
            email="test@tester.com",
            password=password,
        )
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/', data=dict(
            email=user.email,
            password=password,
        ), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login", response.get_data())

        db.session.delete(user)
        db.session.commit()

if __name__ == "__main__":
    app.config['TESTING'] = True
    app.testing = True
    csrf._csrf_disable = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/travis_ci_test'
    app.config['WTF_CSRF_ENABLED'] = False
    db.init_app(app)
    db.create_all()
    unittest.main()
