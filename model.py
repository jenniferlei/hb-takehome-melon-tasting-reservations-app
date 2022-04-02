"""Models for melon tasing reservation scheduler app."""

import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from server import app

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    username = db.Column(db.String, primary_key=True, nullable=False)

    reservation = db.relationship("Reservation", backref="user")

    def __repr__(self):
        return f"<User username={self.username}>"


class Reservation(db.Model):
    """A reservation."""

    __tablename__ = "reservations"
    __table_args__ = (db.UniqueConstraint('username', 'date'),)

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # user = User object
    # (db.relationship("Reservation", backref="user") on User model)

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} username={self.username} date={self.date} start_time={self.start_time} end_time={self.end_time}>"


def connect_to_db(flask_app, db_uri=uri, echo=True):
    """connect to database"""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


def example_data():
    """Create example data for the test database."""
    import crud
    from seed_database import appointment_times
    
    for i in range(50):
        username = f'testuser{i}'
        test_user = crud.create_user(username)
        db.session.add(test_user)

    for idx, time_slot in enumerate(appointment_times):
        username = f'testuser{idx}'
        user = crud.get_user_by_username(username)
        test_reservation = crud.create_reservation(user, "2022-03-31", time_slot[0], time_slot[1])
        db.session.add(test_reservation)
    
    db.session.commit()


if __name__ == "__main__":

    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
