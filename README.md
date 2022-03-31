# Pup Journey

Do you love going on hikes with your dogs? Pup Journey is a platform where any user can search, filter and sort dog-friendly hikes on the west coast. Users can view a hike’s details, including its map location and comments registered users have made. To access additional features, users can create an account and log in. Registered users can create, update and delete pet profiles, hike check ins, bookmarks lists and comments. On the dashboard, users can view a map of all the locations they have visited and a chart of how many miles they have walked and number of hikes they have completed.

![Homepage](/static/img/readme/Pup_Journey_Homepage.png "Homepage")

**CONTENTS**

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Future Features](#future-features)
- [Installation](#installation)
- [About the Developer](#about-the-developer)

## Tech Stack

**Backend:** Python3, Flask, Flask-Marshmallow, Jinja, SQLAlchemy\
**Frontend:** React, React Hooks, JavaScript, HTML5, CSS3, Bootstrap\
**Database:** PostgreSQL\
**API:** Google Maps JavaScript, Google Maps Embed API, Cloudinary API

## Features

### SEARCH HIKES

Users can search for hikes by keyword from the search bar, which filters all hikes in the database.
Alternatively, users can add multiple filters from the off canvas form. When the user clicks Submit, the input from the form is passed to the postgres database asynchronously and returns the results that meet the parameters requested.
Users can sort their results by column, ascending or descending

<details>
  <summary>Click to see gif</summary>
  
<img src="https://user-images.githubusercontent.com/43583599/159387972-7141c4aa-1bef-4867-b09c-b3d5c0c8e055.gif" width="75%" height="75%"/>
</details>

### HIKE DETAILS

Users can view a summary of the hike's details and its map location

<details>
  <summary>Click to see image</summary>
  
<img src="/static/img/readme/Pup_Journey_Hike_Details.png" width="75%" height="75%"/>
</details>

### REGISTRATION, LOG IN, USER SETTINGS & LOG OUT

Users can register, log in, change their user settings, and log out

<details>
  <summary>Click to see gif</summary>
  
<img src="https://user-images.githubusercontent.com/43583599/159392083-f33b1c47-1e36-4d97-9fd9-b2b03d75cd4c.gif" width="75%" height="75%"/>
</details>

### DASHBOARD

Users must register and log in to view the dashboard

#### MAP

Registered users can view a map of locations they have visited and change views by month, year, or all time

<details>
  <summary>Click to see gif</summary>
  
<img src="https://user-images.githubusercontent.com/43583599/159410647-247399dc-2398-4522-ba1a-ed3690402506.gif" width="75%" height="75%"/>
</details>

#### GRAPH

Registered users can view a chart of how many miles they have walked and number of hikes they have completed and change views by month, year, or all time
The chart is created with chart.js

<details>
  <summary>Click to see gif</summary>
  
<img src="https://user-images.githubusercontent.com/43583599/159410658-042082bf-8d11-43a9-b07c-8694cdeb312a.gif" width="75%" height="75%"/>
</details>

### PET PROFILES, BOOKMARKS LISTS, CHECK INS, COMMENTS

Registered users can create, view, update and delete pet profiles, bookmarks lists, check ins and comments from the dashboard, as well as from the search hikes and hike details pages. Any user can see all comments for a hike from the hike details page.
The data for the components are retrieved or modified using fetch requests to Pup Journey's own API endpoints.

<details>
  <summary>Click to see pet profiles</summary>

| Dashboard View                                                                                                     | Search Hikes/Hike Details View                                                                                      |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| <img src="https://user-images.githubusercontent.com/43583599/159401165-9b5fb75a-df84-4464-a9b0-df331671e9ea.gif"/> | <img src="https://user-images.githubusercontent.com/43583599/159401176-6e33f9b5-9907-4dd9-8b0c-b6ff8586cf69.gif" /> |

</details>

<details>
  <summary>Click to see bookmarks lists</summary>

| Dashboard View                                                                                                      | Search Hikes/Hike Details View                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| <img src="https://user-images.githubusercontent.com/43583599/159410557-48d3bf29-9ac7-40a5-a987-9bf57e385b2d.gif" /> | <img src="https://user-images.githubusercontent.com/43583599/159410574-110f815a-a817-4b13-ba17-352ac95bf716.gif" /> |

</details>

<details>
  <summary>Click to see check ins</summary>

| Dashboard View                                                                                                      | Search Hikes/Hike Details View                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| <img src="https://user-images.githubusercontent.com/43583599/159410714-dccf3aa8-d2d9-4f33-95c7-b7a6e8d175fb.gif" /> | <img src="https://user-images.githubusercontent.com/43583599/159410757-f38cec76-a7b4-4f80-a4e1-12b35b384ac2.gif" /> |

</details>

<details>
  <summary>Click to see comments</summary>

Non-registered users can view comments from the hikes and hike details pages.

| Dashboard View                                                                                                      | Search Hikes/Hike Details View                                                                                      |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| <img src="https://user-images.githubusercontent.com/43583599/159410785-1166192f-933d-4cf8-b2cd-3d69d4e7433b.gif" /> | <img src="https://user-images.githubusercontent.com/43583599/159410801-aeab7fb4-86af-49b7-beb3-4b551649ffc7.gif" /> |

</details>

## Future Features

- Trip planning
- Different types of locations (campgrounds, restaurants, etc)
- UI/UX improvements

## Installation

#### Requirements:

- PostgreSQL
- Python 3.7.3

To have this app running on your local computer, please follow the below steps:

Clone repository:

```
$ git clone https://github.com/jenniferlei/Hackbright_Pup_Journey_Project.git
```

Create environmental variables to hold your API keys

```
$ export CLOUDINARY_KEY='{YOUR CLOUDINARY API KEY HERE}'
$ export CLOUDINARY_SECRET='{YOUR CLOUDINARY SECRET HERE}'
$ export GOOGLE_KEY='{YOUR MAPS JS API KEY HERE}'
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

Navigate to `localhost:5000/` to begin your dog-friendly hike search!

## About the Developer

Jennifer Lei is a software engineer in the Greater Los Angeles Area, and previously worked in multiple fields, such as B2B tech sales, finance and e-commerce. A combined love for dogs, hiking, and learning new things (React!) led to the creation of Pup Journey, her capstone project for Hackbright Academy.

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
