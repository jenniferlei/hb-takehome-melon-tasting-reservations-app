# Melon Tasting Reservation Scheduler

A simple service to help users make reservations to go to a fancy melon tasting!

We offer 24/7/365 (including weekends and holidays) but only 1 user can book an appointment on a given day and time.

**CONTENTS**

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [About the Developer](#about-the-developer)

## Tech Stack

**Backend:** Python3, Flask, Flask-Marshmallow, Jinja, SQLAlchemy\
**Frontend:** React, React Hooks, JavaScript, HTML5, CSS3, Bootstrap\
**Database:** PostgreSQL

## Features

### LOG IN

Users can log in by username

### SEARCH OPEN RESERVATIONS | ADD A RESERVATION | VIEW ALL RESERVATIONS

## Installation

#### Requirements:

- PostgreSQL
- Python 3.7.3

To have this app running on your local computer, please follow the below steps:

Clone repository:

```
$ git clone https://github.com/jenniferlei/hb-takehome-melon-tasting-reservations-app.git
```

Create and activate a virtual environment:

```
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate
```

Install dependencies:

```
(env) $ pip3 install -r requirements.txt
```

Create database tables and seed database:

```
(env) $ python3 seed_database.py
```

Start backend server:

```
(env) $ python3 server.py
```

Navigate to `localhost:5000/` to begin making melon tasting reservations!

## About the Developer

Jennifer Lei is a software engineer in the Greater Los Angeles Area, and previously worked in multiple fields, such as B2B tech sales, finance and e-commerce.

Let's connect!

<p><a href="https://www.linkedin.com/in/jenniferlei/">
  <img
    alt="LinkedIn"
    src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white"
  />
</a>
<a href="https://twitter.com/JenniferLei_">
  <img
    alt="Twitter"
    src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white"
  />
</a></p>
