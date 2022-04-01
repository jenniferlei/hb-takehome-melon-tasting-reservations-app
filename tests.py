from unittest import TestCase
from flask import session
from server import app
from model import (connect_to_db, db, example_data, User)
import os

# Only need to do this once to test database:
os.system("dropdb testdb --if-exists")
os.system("createdb testdb")
# Connect to test database
connect_to_db(app, "postgresql:///testdb")
# Create tables and add sample data
db.create_all()
example_data()


class MelonSchedulerTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

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

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")
        
        # # Create tables and add sample data
        # db.create_all()
        # example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login page."""
        result = self.client.post("/login",
                                  data={"username": "user0"},
                                  follow_redirects=True, headers={"Referer": "/"})
        self.assertIn(b"Log Out", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

        # Need a key when testing with sessions
        app.config['SECRET_KEY'] = 'key'

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = "testuser0"
                sess['login'] = True

    def test_dashboard_page(self):
        """Test dashboard page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome, testuser0", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged out of session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

    def test_dashboard_page(self):
        """Test that user can't see dashboard page when logged out."""

        result = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Log in to start making your melon tasting reservation today", result.data)


class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = "testuser0"
                sess['login'] = True

    def test_login(self):
        """Test log in form.

        Unlike login test above, 'with' is necessary here in order to refer to session.
        """

        with self.client as c:
            
            result = c.post('/login',
                            data={"username": "testuser0"},
                            follow_redirects=True,
                            headers={"Referer": "/"}
                            )
            self.assertEqual(session['username'], 'testuser0')
            self.assertEqual(session['login'], True)
            self.assertIn(b"Welcome back", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser0'

            result = c.get("/logout",
                            follow_redirects=True,
                            headers={"Referer": "/"})

            self.assertNotIn(b'username', session)
            self.assertNotIn(b'login', session)
            # print("LINE 207", result.data)
            self.assertIn(b'Successfully logged out!', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
