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
        flash("User does not exist.")
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



@app.route("/reservations")
def all_reservations():
    """View all reservations for a given user."""

    username = session.get("username")
    reservations = crud.get_reservations_by_user(username)
    reservations_schema = ReservationSchema(many=True)
    reservations_json = reservations_schema.dump(reservations)

    return jsonify({"reservations": reservations_json})


@app.route("/search_reservations", methods=["GET"])
def search_reservations():
    """Search for reservations"""

    date = request.args.get("date", "")
    start_time = request.args.get("start_time", "")
    end_time = request.args.get("end_time", "")

    reservations = crud.get_reservations_by_query(date, start_time, end_time)
    reservations_schema = ReservationSchema(many=True)
    reservations_json = reservations_schema.dump(reservations)

    return jsonify({"reservations": reservations_json})


@app.route("/login_session.json")
def login_session_json():
    """Return a JSON response for a login."""

    username = session.get("username")

    login = "False"

    if username:
        login = "True"

    return jsonify({"login": login, "username": username})



@app.route("/add-pet", methods=["POST"])
def add_pet():
    """Create a pet profile"""

    logged_in_email = session.get("user_email")
    user = crud_users.get_user_by_email(logged_in_email)

    form_data = request.form.to_dict("formData")
    pet_name = form_data["petName"]
    gender = form_data["gender"]
    birthday = form_data["birthday"]
    breed = form_data["breed"]
    my_file = request.files.get("imageFile")

    if gender == "":
        gender = None
    if birthday == "":
        birthday = None
    if breed == "":
        breed = None
    if my_file is None:
        pet_img_url = None
        img_public_id = None
    else:
        # save the uploaded file to Cloudinary by making an API request
        result = cloudinary.uploader.upload(
            my_file,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME,
        )
        pet_img_url = result["secure_url"]
        img_public_id = result["public_id"]

    check_ins = []

    pet = crud_pets.create_pet(
        user,
        pet_name,
        gender,
        birthday,
        breed,
        pet_img_url,
        img_public_id,
        check_ins,
    )
    db.session.add(pet)
    db.session.commit()
    

    pet_schema = PetSchema()
    pet_json = pet_schema.dump(pet)

    return jsonify({"success": True, "petAdded": pet_json})


@app.route("/edit-pet/<pet_id>", methods=["POST"])
def edit_pet(pet_id):
    """Edit a pet"""

    pet = crud_pets.get_pet_by_id(pet_id)

    form_data = request.form.to_dict("formData")

    pet.pet_name = form_data["petName"]

    gender = form_data["gender"]
    birthday = form_data["birthday"]
    breed = form_data["breed"]
    my_file = request.files.get("imageFile")

    print(my_file)

    if gender != "":
        pet.gender = gender
    if birthday != "":
        pet.birthday = birthday
    if breed != "":
        pet.breed = breed

    if my_file is not None: # if user uploads new image file, delete old image from cloudinary
    # then upload new image
        img_public_id = pet.img_public_id
        if img_public_id is not None:
            cloudinary.uploader.destroy(
                img_public_id,
                api_key=CLOUDINARY_KEY,
                api_secret=CLOUDINARY_SECRET,
                cloud_name=CLOUD_NAME,
        )
        # save the uploaded file to Cloudinary by making an API request
        result = cloudinary.uploader.upload(
            my_file,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME,
        )

        pet.pet_imgURL = result["secure_url"]
        pet.img_public_id = result["public_id"]

    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-pet/<pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    """Delete a pet profile"""

    pet = crud_pets.get_pet_by_id(pet_id)
    img_public_id = pet.img_public_id
    if img_public_id is not None:
        cloudinary.uploader.destroy(
            img_public_id,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME,
        )

    pet.check_ins.clear()

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/hikes/<hike_id>/add-check-in", methods=["POST"])
def add_hike_check_in(hike_id):
    """Add check in for a hike."""

    # logged_in_email = session.get("user_email")
    # user = crud_users.get_user_by_email(logged_in_email)
    hike = crud_hikes.get_hike_by_id(hike_id)
    pets_checked = request.get_json().get("allPetOptions") # list of objects (select, pet_name, pet_id)
    date_hiked = request.get_json().get("dateHiked")
    miles_completed = request.get_json().get("milesCompleted")
    total_time = request.get_json().get("totalTime")
    notes = request.get_json().get("notes")

    if total_time == "":
        total_time = None

    pets_to_check_in = []
    pets_not_checked_in = []

    for pet in pets_checked:
        select, _, pet_id = pet
        pet_obj = crud_pets.get_pet_by_id(pet[pet_id])
        if pet[select] is True:
            pets_to_check_in.append(pet_obj)
        else:
            pets_not_checked_in.append(pet_obj)

    check_in = crud_check_ins.create_check_in(
        hike,
        pets_to_check_in,
        date_hiked,
        miles_completed,
        total_time,
        notes
    )

    db.session.add(check_in)
    db.session.commit()

    check_in_schema = CheckInSchema()
    check_in_json = check_in_schema.dump(check_in)

    return jsonify({"checkInAdded": check_in_json})


@app.route("/add-check-in", methods=["POST"])
def add_check_in():
    """Add check in for a hike."""

    # logged_in_email = session.get("user_email")
    # user = crud_users.get_user_by_email(logged_in_email)
    hike_id = request.get_json().get("hikeId")
    pets_checked = request.get_json().get("allPetOptions") # list of objects (select, pet_name, pet_id)
    date_hiked = request.get_json().get("dateHiked")
    miles_completed = request.get_json().get("milesCompleted")
    total_time = request.get_json().get("totalTime")
    notes = request.get_json().get("notes")

    hike = crud_hikes.get_hike_by_id(hike_id)

    if total_time == "":
        total_time = None

    pets_to_check_in = []
    pets_not_checked_in = []

    for pet in pets_checked:
        select, _, pet_id = pet
        pet_obj = crud_pets.get_pet_by_id(pet[pet_id])
        if pet[select] is True:
            pets_to_check_in.append(pet_obj)
        else:
            pets_not_checked_in.append(pet_obj)

    check_in = crud_check_ins.create_check_in(
        hike,
        pets_to_check_in,
        date_hiked,
        miles_completed,
        total_time,
        notes
    )

    db.session.add(check_in)
    db.session.commit()

    check_in_schema = CheckInSchema(only=["check_in_id","date_hiked","hike_id","miles_completed","notes","pets","total_time","hike.hike_name","hike.latitude","hike.longitude"])
    check_in_json = check_in_schema.dump(check_in)

    return jsonify({"checkInAdded": check_in_json})


@app.route("/edit-check-in/<check_in_id>", methods=["POST"])
def edit_check_in(check_in_id):
    """Edit a check in"""

    pets_to_add = request.get_json().get("addPet")
    pets_to_remove = request.get_json().get("removePet")
    date_hiked = request.get_json().get("dateHiked")
    miles_completed = request.get_json().get("milesCompleted")
    total_time = request.get_json().get("totalTime")
    notes = request.get_json().get("notes")

    for pet in pets_to_add: # Add pets to check in
        select, _, pet_id = pet
        if pet[select] is True:
            pet_check_in = crud_pets_check_ins.create_pet_check_in(pet[pet_id], check_in_id)
            db.session.add(pet_check_in)

    for pet in pets_to_remove: # Remove pets from check in
        select, _, pet_id = pet
        if pet[select] is True:
            pet_check_in = crud_pets_check_ins.get_pet_check_in_by_pet_id_check_in_id(pet[pet_id], check_in_id)
            db.session.delete(pet_check_in)

    check_in = crud_check_ins.get_check_ins_by_check_in_id(check_in_id)

    if date_hiked == "": # if date_hiked is left blank, use previous date_hiked
        date_hiked = check_in.date_hiked

    if miles_completed == "": # if miles_completed is left blank, use previous miles_completed
        miles_completed = check_in.miles_completed

    if total_time == "": # if total_time is left blank, use previous total_time
        total_time = check_in.total_time

    check_in.date_hiked = date_hiked
    check_in.miles_completed = miles_completed
    check_in.total_time = total_time
    check_in.notes = notes

    if check_in.pets == []: # if there are no pets after pets have been updated, delete check in
        db.session.delete(check_in)

    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-check-in/<check_in_id>", methods=["DELETE"])
def delete_check_in(check_in_id):
    """Delete a check-in"""

    logged_in_email = session.get("user_email")

    check_in = crud_check_ins.get_check_ins_by_check_in_id(check_in_id)
    check_in.pets.clear()

    db.session.delete(check_in)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-pet-check-in", methods=["POST"])
def delete_pet_check_in():
    """Remove a check-in from a pet"""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to delete a check in.")
    else:
        pet_id, check_in_id = request.form.get("delete").split(",")
        pet_check_in = crud_pets_check_ins.get_pet_check_in_by_pet_id_check_in_id(pet_id, check_in_id)
        check_in = crud_check_ins.get_check_ins_by_check_in_id(check_in_id)
        pet = crud_pets.get_pet_by_id(pet_id)

        flash(
            f"Success! Check in at {check_in.hike.hike_name} by {pet.pet_name} has been deleted."
        )

        db.session.delete(pet_check_in)
        db.session.commit()

    return redirect(request.referrer)


@app.route("/create-bookmarks-list", methods=["POST"])
def create_bookmarks_list():
    """Create a bookmark list"""

    user = crud_users.get_user_by_email(session["user_email"])
    bookmarks_list_name = request.get_json().get("bookmarksListName")
    hikes = []

    bookmarks_list = crud_bookmarks_lists.create_bookmarks_list(
        bookmarks_list_name, user.user_id, hikes
    )

    db.session.add(bookmarks_list)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/edit-bookmarks-list/<bookmarks_list_id>", methods=["POST"])
def edit_bookmarks_list(bookmarks_list_id):
    """Edit a bookmark list"""

    bookmarks_list = crud_bookmarks_lists.get_bookmarks_list_by_bookmarks_list_id(
        bookmarks_list_id
    )
    bookmarks_list.bookmarks_list_name = request.get_json().get("bookmarksListName")

    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-bookmarks-list/<bookmarks_list_id>", methods=["DELETE"])
def delete_bookmarks_list(bookmarks_list_id):
    """Delete a bookmarks list"""

    bookmarks_list = crud_bookmarks_lists.get_bookmarks_list_by_bookmarks_list_id(
        bookmarks_list_id
    )
    bookmarks_list.hikes.clear()

    db.session.delete(bookmarks_list)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/<bookmarks_list_id>/add-hikes", methods=["POST"])
def add_hikes_to_existing_bookmarks_list(bookmarks_list_id):
    """Add hikes to an existing bookmarks list"""

    # hike = crud_hikes.get_hike_by_id(hike_id)
    hikes = request.get_json().get("allHikesOptions") # this will get a list of objects
    print(hikes)
    bookmarks_list = crud_bookmarks_lists.get_bookmarks_list_by_bookmarks_list_id(bookmarks_list_id)
    bookmarks_list_hikes = bookmarks_list.hikes
    print(bookmarks_list)
    print(bookmarks_list_hikes)

    for hike in hikes:
        hike_obj = crud_hikes.get_hike_by_id(hike["hike_id"])
        if hike["select"] is True and hike_obj not in bookmarks_list_hikes:
            # if selected and already a connection, create connection
            hike_bookmark = crud_hikes_bookmarks_lists.create_hike_bookmarks_list(hike["hike_id"], bookmarks_list_id)
            db.session.add(hike_bookmark)
        elif hike["select"] is False and hike_obj in bookmarks_list_hikes:
            # if unselected and there's a connection, delete connection
            hike_bookmarks = crud_hikes_bookmarks_lists.get_hike_bookmarks_list_by_hike_id_bookmarks_list_id(hike["hike_id"], bookmarks_list_id)
            for hike_bookmark in hike_bookmarks:
                db.session.delete(hike_bookmark)

    db.session.commit()

    return jsonify({"success": True})


@app.route("/hikes/<hike_id>/add-hike-to-existing-list", methods=["POST"])
def add_hike_to_existing_bookmarks_list(hike_id):
    """Add hike to an existing bookmarks list"""

    hike = crud_hikes.get_hike_by_id(hike_id)
    bookmarks_list_options = request.get_json().get("allBookmarksListOptions") # this will get a list of objects

    for bookmarks_list in bookmarks_list_options:
        bookmarks_list_obj = crud_bookmarks_lists.get_bookmarks_list_by_bookmarks_list_id(bookmarks_list["bookmarks_list_id"])
        bookmarks_list_hikes = bookmarks_list_obj.hikes
        if bookmarks_list["select"] is True and hike not in bookmarks_list_hikes:
            # if selected, check if there's already a connection, else add connection
            hike_bookmark = crud_hikes_bookmarks_lists.create_hike_bookmarks_list(hike_id, bookmarks_list["bookmarks_list_id"])
            db.session.add(hike_bookmark)
        elif bookmarks_list["select"] is False and hike in bookmarks_list_hikes:
            # if unselected and there's a connection, delete connection
            hike_bookmarks = crud_hikes_bookmarks_lists.get_hike_bookmarks_list_by_hike_id_bookmarks_list_id(hike_id, bookmarks_list["bookmarks_list_id"])
            for hike_bookmark in hike_bookmarks:
                db.session.delete(hike_bookmark)

    db.session.commit()

    return jsonify({"success": True})


@app.route("/hikes/<hike_id>/add-hike-to-new-list", methods=["POST"])
def add_hike_to_new_bookmarks_list(hike_id):
    """Add hike to a new bookmarks list"""

    logged_in_email = session.get("user_email")
    user = crud_users.get_user_by_email(logged_in_email)

    bookmarks_list_name = request.get_json().get("bookmarksListName")
    hikes = [crud_hikes.get_hike_by_id(hike_id)]
    hike_bookmark = crud_bookmarks_lists.create_bookmarks_list(
        bookmarks_list_name, user.user_id, hikes
    )

    db.session.add(hike_bookmark)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/<bookmarks_list_id>/<hike_id>/remove-hike", methods=["DELETE"])
def remove_hike(bookmarks_list_id, hike_id):
    """Delete a hike from a bookmarks list"""

    hike = crud_hikes.get_hike_by_id(hike_id)
    bookmarks_list = crud_bookmarks_lists.get_bookmarks_list_by_bookmarks_list_id(
        bookmarks_list_id
    )
    hikes_bookmarks_lists = crud_hikes_bookmarks_lists.get_hike_bookmarks_list_by_hike_id_bookmarks_list_id(
        hike_id, bookmarks_list_id
    )

    for hikes_bookmarks_list in hikes_bookmarks_lists:
        db.session.delete(hikes_bookmarks_list)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/hikes/<hike_id>/add-comment", methods=["POST"])
def add_hike_comment(hike_id):
    """Add a comment for a hike"""
    logged_in_email = session.get("user_email")

    user = crud_users.get_user_by_email(logged_in_email)
    hike = crud_hikes.get_hike_by_id(hike_id)
    comment_body = request.get_json().get("comment_body")

    comment = crud_comments.create_comment(
        user, hike, comment_body, date_created=datetime.now(), edit=False, date_edited=None
    )
    db.session.add(comment)
    db.session.commit()

    comment_schema = CommentSchema()
    comment_json = comment_schema.dump(comment)

    return jsonify({"commentAdded": comment_json, "login": True})


@app.route("/add-comment", methods=["POST"])
def add_comment():
    """Add a comment for a hike"""
    logged_in_email = session.get("user_email")

    user = crud_users.get_user_by_email(logged_in_email)
    hike_id = request.get_json().get("hikeId")
    hike = crud_hikes.get_hike_by_id(hike_id)
    comment_body = request.get_json().get("commentBody")

    comment = crud_comments.create_comment(
        user, hike, comment_body, date_created=datetime.now(), edit=False, date_edited=None
    )
    db.session.add(comment)
    db.session.commit()

    comment_schema = CommentSchema()
    comment_json = comment_schema.dump(comment)

    return jsonify({"commentAdded": comment_json, "login": True})


@app.route("/edit-comment/<comment_id>", methods=["POST"])
def edit_comment(comment_id):
    """Edit a comment"""

    comment = crud_comments.get_comment_by_comment_id(comment_id)
    comment.body = request.get_json().get("commentBody")
    comment.edit = True
    comment.date_edited = datetime.now()

    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete-comment/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """Delete a comment"""

    comment = crud_comments.get_comment_by_comment_id(comment_id)

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"success": True})



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
