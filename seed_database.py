"""Script to seed database."""

import os
# import json
# from random import choice, randint
# from datetime import datetime

import crud
import model
import server

# Run dropdb and createdb to re-create database
os.system("dropdb scheduler --if-exists")
os.system("createdb scheduler")

# Connect to the database and call db.create_all
model.connect_to_db(server.app)
model.db.create_all()

test_user = crud.create_user("user")
test_user2 = crud.create_user("user2")
reservation = crud.create_reservation(test_user, "2022-03-31", "12:00", "12:30")

model.db.session.add_all([test_user, test_user2])

model.db.session.commit()
