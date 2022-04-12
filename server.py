"""Server for melon tasing reservation scheduler app."""

from flask import Flask, render_template, json, jsonify, request, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os

from model import (connect_to_db, db, User, Reservation)

import crud

from jinja2 import StrictUndefined

from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
ma = Marshmallow(app)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    reservations = fields.List(fields.Nested("ReservationSchema", exclude=("user",)))


class ReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation
        include_fk = True
        load_instance = True


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login"""
    username = request.form.get("username")

    user = crud.get_user_by_username(username)
    if not user:
        user = crud.create_user(username)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        session["login"] = True
        flash(f"Welcome, {user.username}!")
    else:
        # Log in user by storing the user's email in session
        session["username"] = user.username
        session["login"] = True
        flash(f"Welcome back, {user.username}!")

    return redirect(request.referrer)


@app.route("/logout")
def process_logout():
    """Log user out of site.

    Delete the login session
    """

    del session["login"]
    del session["username"]
    flash("Successfully logged out!")
    return redirect(request.referrer)


@app.route("/login_session.json")
def login_session_json():
    """Return a JSON response for a login."""

    username = session.get("username")

    login = "False"

    if username:
        login = "True"

    return jsonify({"login": login, "username": username})


@app.route("/reservations.json")
def all_reservations():
    """Return a JSON response for all reservations for logged in user."""

    username = session.get("username")
    reservations = crud.get_reservations_by_user(username)
    reservations_schema = ReservationSchema(many=True)
    reservations_json = reservations_schema.dump(reservations)

    return jsonify({"reservations": reservations_json})


@app.route("/search_reservations", methods=["GET"])
def search_reservations():
    """Return a JSON response for reservations given date and time queries"""

    date = request.args.get("date", "")
    start_time = request.args.get("start_time", "")
    end_time = request.args.get("end_time", "")

    reservations = crud.get_reservations_by_query(date, start_time, end_time)
    reservations_schema = ReservationSchema(many=True)
    reservations_json = reservations_schema.dump(reservations)

    return jsonify({"reservations": reservations_json})


@app.route("/add-reservation", methods=["POST"])
def add_reservation():
    """Create a reservation"""

    username = session.get("username")
    user = crud.get_user_by_username(username)

    date = request.get_json().get("date")
    start_time = request.get_json().get("startTime")
    end_time = request.get_json().get("endTime")

    reservation = crud.create_reservation(user, date, start_time, end_time)
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-reservation/<reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    """Delete a reservation"""

    reservation = crud.get_reservations_by_id(reservation_id)

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"success": True})


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

connect_to_db(app)