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


def connect_to_db(flask_app, db_uri="postgresql://evseexcyzaukhk:920fdfe2d7b0cb909504ad61587075e1fed59b38b12a5a949cd17d02755bad73@ec2-3-217-251-77.compute-1.amazonaws.com:5432/dcvr918o9v4v2d", echo=True):
    """connect to database"""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    # flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
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
