"""Models for melon tasing reservation scheduler app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


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


def connect_to_db(flask_app, db_uri="postgresql:///scheduler", echo=True):
    """connect to database"""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


def example_data():
    """Create example data for the test database."""
    
    test_user = User(username="testuser")
    test_reservation = Reservation(user=test_user, date="2022-03-31", start_time="12:00", end_time="12:30")
    
    db.session.add_all([test_user, test_reservation])
    db.session.commit()


if __name__ == "__main__":

    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
