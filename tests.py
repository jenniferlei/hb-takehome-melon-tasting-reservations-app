from unittest import TestCase
from flask import session
from server import app
from model import (connect_to_db, db, example_data, User)
import os

os.system("dropdb testdb --if-exists")
os.system("createdb testdb")

# # Connect to test database
# connect_to_db(app, "postgresql:///testdb")

# # Create tables and add sample data
# db.create_all()
# example_data()


class PupJourneyTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Need a key when testing with sessions
        app.config['SECRET_KEY'] = 'key' 

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data

        db.create_all()
        test_user = User(full_name="Test User 1", email="test@test", password="test")

        print(test_user)

        db.session.add(test_user)
        db.session.commit()

        print(test_user)

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login page."""
        # print('HELLO!')
        result = self.client.post("/login",
                                  data={"email": "test@test", "current-password": "test"},
                                  follow_redirects=True, headers={"Referer": "/"})
        # print(result.data, "RESULT STATUS CODE")
        self.assertIn(b"Log Out", result.data)

    def test_hike_details(self):
        """Test hike details page."""
        result = self.client.get("/hikes/1")
        self.assertIn(b"Cedar Grove and Vista View Point in Griffith Park", result.data)

    def test_all_hikes(self):
        """Test all hikes page."""

        result = self.client.get("/hikes")
        self.assertIn(b"Cedar Grove and Vista View Point in Griffith Park", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

        # Need a key when testing with sessions
        app.config['SECRET_KEY'] = 'key' 

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = "test@test"
                sess['login'] = True

    def test_dashboard_page(self):
        """Test dashboard page."""

        result = self.client.get("/dashboard") # the result is not showing all the stuff from React
        self.assertIn(b"Where We've Been", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged out of session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#     def test_dashboard_page(self):
#         """Test that user can't see dashboard page when logged out."""

#         result = self.client.get("/dashboard", follow_redirects=True)
#         self.assertNotIn(b"Dashboard", result.data)
#         self.assertIn(b"You must log in to view your dashboard.", result.data)


# class FlaskTestsLogInLogOut(TestCase):  # Bonus example. Not in lecture.
#     """Test log in and log out."""

#     def setUp(self):
#         """Before every test"""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#     def test_login(self):
#         """Test log in form.

#         Unlike login test above, 'with' is necessary here in order to refer to session.
#         """

#         with self.client as c:
#             result = c.post('/login',
#                             data={"email": "test@test", 'current-password': 'test'},
#                             follow_redirects=True
#                             )
#             self.assertEqual(session['user_email'], 'test@test')
#             self.assertIn(b"Welcome back", result.data)

#     def test_logout(self):
#         """Test logout route."""

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['email'] = 'test@test'

#             result = self.client.get('/logout', follow_redirects=True)

#             self.assertNotIn(b'email', session)
#             self.assertIn(b'Successfully logged out!', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
