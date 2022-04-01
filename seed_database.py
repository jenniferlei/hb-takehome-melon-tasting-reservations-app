"""Script to seed database."""

import os
# import json
# from random import choice, randint
# from datetime import datetime

import crud
import model
import server

# # Run dropdb and createdb to re-create database
# os.system("dropdb scheduler --if-exists")
# os.system("createdb scheduler")

# Connect to the database and call db.create_all
model.connect_to_db(server.app)
model.db.create_all()

appointment_times = [
  ["00:00", "00:30", 1],
  ["00:30", "01:00", 2],
  ["01:00", "01:30", 3],
  ["01:30", "02:00", 4],
  ["02:00", "02:30", 5],
  ["02:30", "03:00", 6],
  ["03:00", "03:30", 7],
  ["03:30", "04:00", 8],
  ["04:00", "04:30", 9],
  ["04:30", "05:00", 10],
  ["05:00", "05:30", 11],
  ["05:30", "06:00", 12],
  ["06:00", "06:30", 13],
  ["06:30", "07:00", 14],
  ["07:00", "07:30", 15],
  ["07:30", "08:00", 16],
  ["08:00", "08:30", 17],
  ["08:30", "09:00", 18],
  ["09:00", "09:30", 19],
  ["09:30", "10:00", 20],
  ["10:00", "10:30", 21],
  ["10:30", "11:00", 22],
  ["11:00", "11:30", 23],
  ["11:30", "12:00", 24],
  ["12:00", "12:30", 25],
  ["12:30", "13:00", 26],
  ["13:00", "13:30", 27],
  ["13:30", "14:00", 28],
  ["14:00", "14:30", 29],
  ["14:30", "15:00", 30],
  ["15:00", "15:30", 31],
  ["15:30", "16:00", 32],
  ["16:00", "16:30", 33],
  ["16:30", "17:00", 34],
  ["17:00", "17:30", 35],
  ["17:30", "18:00", 36],
  ["18:00", "18:30", 37],
  ["18:30", "19:00", 38],
  ["19:00", "19:30", 39],
  ["19:30", "20:00", 40],
  ["20:00", "20:30", 41],
  ["20:30", "21:00", 42],
  ["21:00", "21:30", 43],
  ["21:30", "22:00", 44],
  ["22:00", "22:30", 45],
  ["22:30", "23:00", 46],
  ["23:00", "23:30", 47],
  ["23:30", "24:00", 48],
]

for i in range(50):
    username = f'user{i}'
    test_user = crud.create_user(username)
    model.db.session.add(test_user)

for idx, time_slot in enumerate(appointment_times):
    username = f'user{idx}'
    user = crud.get_user_by_username(username)
    test_reservation = crud.create_reservation(user, "2022-03-31", time_slot[0], time_slot[1])
    model.db.session.add(test_reservation)

model.db.session.commit()
