import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import Movies, Actors, setup_db
# import json


def create_app(test_config=None):

  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,PUT,DELETE,OPTIONS')
        return response

    @app.route('/')
    def home_page():

        return jsonify({
            'message': 'Welcome to Casting Agency'
        }), 200

    '''
    Actors Endpoint
    
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(payload):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name is None \
                or age is None \
                or gender is None:
            abort(400)
        try:

            actor = Actors(
                name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'created': actor.id,
                'message': 'Actor created'
            }), 201
        except Exception as error:
            abort(422)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            selection = Actors.query.order_by(Actors.id).all()
            actors = [actors.format() for actors in selection]
            return jsonify({
                'success': True,
                'actors': actors,
                'total_actors': len(Actors.query.all())
            }), 200
        except Exception as err:
            print(err)
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            name = request.json.get('name')
            if type(name) is not str or len(name) is 0:
                abort(400)

            actor.name = name
            actor.update()
            return jsonify({
                'success': True,
                'actor': [actor.format()],
            }), 200
        except Exception as err:
            print(err)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_Actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:

            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor.id,
                'message': 'Actor deleted'
            })
        except Exception as err:
            print(err)
            abort(500)
    '''
    Movies Endpoint
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if title is None \
                or release_date is None:
            abort(400)
        try:

            movie = Movies(
                title=title, release_date=release_date)
            movie.insert()
            return jsonify({
                'success': True,
                'created': movie.id,
                'message': 'Movie created'
            }), 201
        except Exception as error:
            print(error)
            abort(422)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            selection = Movies.query.order_by(Movies.id).all()
            movies = [movies.format() for movies in selection]
            return jsonify({
                'success': True,
                'movies': movies,
                'total_movies': len(Movies.query.all())
            }), 200
        except Exception as err:
            print(err)
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            title = request.json.get('title')
            if type(title) is not str or len(title) is 0:
                abort(400)

            movie.title = title
            movie.update()
            return jsonify({
                'success': True,
                'movie': [movie.format()],
            })
        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:

            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie.id,
                'message': 'Movie deleted'
            })
        except Exception as err:
            print(err)
            abort(500)

    # Error Handling
    # handle not found resources
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    # handle unprocessable entities
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    # handle internal server errors
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''

    # handle user inputs
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    # handle unauthorized request errors
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized access",
        }), 401

    # handle forbidden requests
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Request Forbidden",
        }), 403

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
