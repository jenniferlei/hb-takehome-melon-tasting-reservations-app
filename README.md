# Melon Tasting Reservation Scheduler

A simple service to help users make reservations to go to a fancy melon tasting!

We offer 24/7/365 (including weekends and holidays) but only 1 user can book an appointment on a given day and time.

<img width="75%" height="75%" alt="Homepage" src="https://user-images.githubusercontent.com/43583599/161311049-ba6b92be-bf91-473e-a77c-cde7daf0039d.png">

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
<br/>The login form sends a post request to the Python-Flask backend and saves the session username and login information

<img width="50%" height="50%" alt="Log In" src="https://user-images.githubusercontent.com/43583599/161312093-51c658a9-a7fc-4cf4-bf9b-9dd23b8193ab.png">

### RESERVATIONS

<img width="50%" height="50%" alt="Reservations" src="https://user-images.githubusercontent.com/43583599/161316789-855175d2-ff7d-4dbe-986f-9c77f617bbd0.png">

#### VIEW ALL RESERVATIONS

Logged in users can view a table of their own reservations on the right side of the page
<br/>React's useEffect hook fetches the JSON response for the logged in user's reservations from the Python-Flask backend server

#### SEARCH AVAILABLE RESERVATIONS

Logged in users can search reservations by date and optional start/end times
<br/>The search sends a get fetch request to the Python-Flask backend server and returns a JSON response to the React frontend
<br/><img width="50%" height="50%" alt="Search Reservations" src="https://user-images.githubusercontent.com/43583599/161325781-d234b098-5bc0-42b0-a8dd-43503c703666.png">

If the user searches for reservations on a date they already have a reservation or if there are no reservations available, the search will not return any search results

| Existing Reservation on Search Date | No Available Reservations in Search Time Frame |
| ----------------------------------- | ---------------------------------------------- |
| <img src="https://user-images.githubusercontent.com/43583599/161316945-6b642709-9b4d-4d01-a7ff-f9635a3b131e.png"> | <img src="https://user-images.githubusercontent.com/43583599/161325463-3ee999ad-064e-45f4-9c29-0455694e5f5b.png"> |

#### ADD A RESERVATION

Logged in users can select an available reservation from the search results and make a reservation
<br/>When the user confirms, a post request is sent to the Python-Flask backend and adds a new reservation into the postgreSQL database
<br/><img width="50%" height="50%" alt="Add Reservation" src="https://user-images.githubusercontent.com/43583599/161326381-b93bf406-feeb-4efe-9dfd-f0269c4576f8.png">

#### DELETE A RESERVATION

Logged in users can delete a reservation from their existing reservations
<br/>When the user confirms, a delete request is sent to the Python-Flask backend and the existing reservation is deleted from the postgreSQL database
<br/><img width="50%" height="50%" alt="Delete Reservation" src="https://user-images.githubusercontent.com/43583599/161327585-ce150742-4d1a-4f03-b49b-17f7772928b1.png">


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
