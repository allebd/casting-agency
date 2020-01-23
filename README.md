# Casting Agency

## Introduction

Flask App for creating movies and managing and assigning actors to those movies.

## Table of Contents

* [Introduction](#introduction)
* [Heroku Deployment](#heroku-deployment)
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)
* [Acknowledgements](#acknowledgements)
* [Author](#author)

## Heroku Deployment

Application was deployed to Heroku. Use public URL [https://casting-agency-allebd.herokuapp.com](https://casting-agency-allebd.herokuapp.com) with API endpoints.

## Technologies Used

Below are the key dependencies

* [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Getting started

### Clone

* Clone this project to your local machine `https://github.com/allebd/casting-agency.git`

```bash
   git clone https://github.com/allebd/casting-agency.git
```

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql casting < casting.psql
```

### Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
./setup.sh
flask run
```

### Endpoints

| METHOD | DESCRIPTION            | ENDPOINTS
| ------ | ---------------------- | ---------------------
| GET    | Get all movies         | `/movies`
| GET    | Get a movie by id      | `/movies/:movie_id`
| POST   | Create a movie         | `/movies`
| PATCH  | Update a movie         | `/movies/:movie_id`
| DELETE | Delete a movie         | `/movies/:movie_id`
| GET    | Get all actors         | `/actors`
| GET    | Get an actor by id     | `/actors/:actor_id`
| POST   | Create an actor        | `/actors`
| PATCH  | Update an actor        | `/actors/:actor_id`
| DELETE | Delete an actor        | `/actors/:actor_id`

```bash
GET '/movies'
- Fetches a list of all movies the database
- Request Arguments: None
- Returns: An object with a keys: success, movies and total_movies
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 02 Feb 2019 00:00:00 GMT",
      "title": "Gemini Man"
    },
    {
      "id": 2,
      "release_date": "Mon, 03 Mar 2014 00:00:00 GMT",
      "title": "Home Alone"
    }
  ],
  "success": true,
  "total_movies": 2
}

***********************************************************************************************************************************

GET '/movies/{movie_id}'
- Fetches a movie the database
- Request Arguments: movie_id
- Returns: An object with a keys: success, movie
{
  "movie": [
    {
      "id": 1,
      "release_date": "Sat, 02 Feb 2019 00:00:00 GMT",
      "title": "Home Alone"
    }
  ],
  "success": true
}

***********************************************************************************************************************************

POST '/movies'
- Creates a movie in the database
- Request Arguments:
    {
        "title": <str>,
        "release_date": <str>,
    }
- Returns: A dictionary containing a success message if the operation was successful
{
  "message": "movie successfully added",
  "success": true,
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 02 Feb 2019 00:00:00 GMT",
      "title": "Gemini Man"
    },
    {
      "id": 2,
      "release_date": "Mon, 03 Mar 2014 00:00:00 GMT",
      "title": "Home Alone"
    }
  ]
}

***********************************************************************************************************************************

PATCH '/movies/{movie_id}'
- Edits a movie from the database
- Request Arguments: movie_id
- Returns: A dictionary containing a success message if the operation was successful

{
  "movie": [
    {
      "id": 1,
      "release_date": "Sat, 02 Feb 2019 00:00:00 GMT",
      "title": "Home Alone"
    }
  ],
  "success": true,
  "message": 'movie successfully updated'
}

***********************************************************************************************************************************

DELETE '/movies/{movie_id}'
- Deletes a movie from the database
- Request Arguments: movie_id
- Returns: A dictionary containing a success message if the operation was successful

{
  "deleted": 2,
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 02 Feb 2019 00:00:00 GMT",
      "title": "Gemini Man"
    },
    {
      "id": 2,
      "release_date": "Mon, 03 Mar 2014 00:00:00 GMT",
      "title": "Home Alone"
    }
  ],
  "success": true,
  "total_movies": 2
}

***********************************************************************************************************************************

GET '/actors'
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding string of the actor
- Request Arguments: None
- Returns: An object with a single key, actors, that contains a object of key:value pairs.
{
  "actors": [
    {
      "age": 43,
      "gender": "male",
      "id": 1,
      "name": "Ryan Reynolds"
    },
    {
      "age": 34,
      "gender": "male",
      "id": 2,
      "name": "Dave Franco"
    },
  ],
  "success": true,
  "total_actors": 2
}

***********************************************************************************************************************************

GET '/actors/{actor_id}'
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding string of the actor
- Request Arguments: actor_id
- Returns: An object with a single key, actors, that contains a object of key:value pairs.
{
  "actor": [
    {
      "age": 43,
      "gender": "male",
      "id": 1,
      "name": "Ryan Reynolds"
    }
  ],
  "success": true
}

***********************************************************************************************************************************

POST '/actors'
- Creates a new actor in the database
- Request Arguments:
        {
            "name": <str>,
            "gender": <str>,
            "age": <int>
        }
- Returns: A dictionary containing a success message if the operation was successful
{
  "message": "movie successfully added",
  "success": true,
  "actors": [
    {
      "age": 43,
      "gender": "male",
      "id": 1,
      "name": "Ryan Reynolds"
    },
    {
      "age": 34,
      "gender": "male",
      "id": 2,
      "name": "Dave Franco"
    },
  ]
}

***********************************************************************************************************************************

PATCH '/actors/{actor_id}'
- Edits an actor  from the database
- Request Arguments: actor_id
- Returns: A dictionary containing a success message if the operation was successful

{
  "actor": [
    {
      "age": 34,
      "gender": "male",
      "id": 2,
      "name": "Dave Franco"
    }
  ],
  "success": true,
  "message": 'actor successfully updated'
}

***********************************************************************************************************************************

DELETE '/actors/{actor_id}'
- Deletes an actor from the database
- Request Arguments: actor_id
- Returns: A dictionary containing a success message if the operation was successful

{
  "deleted": 2,
  "actors": [
    {
      "age": 43,
      "gender": "male",
      "id": 1,
      "name": "Ryan Reynolds"
    },
    {
      "age": 34,
      "gender": "male",
      "id": 2,
      "name": "Dave Franco"
    },
  ],
  "success": true,
  "total_actors": 2
}
```

### Running Unit Test

To run tests, execute:

```bash
dropdb casting_test && createdb casting_test
./setup_test.sh
```

## Acknowledgements

* [Udacity](https://udacity.com/)

## Author

[Bella Oyedele](https://github.com/allebd)
