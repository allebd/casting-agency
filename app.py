import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
from utils import validate_movie, validate_actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/')
    def retrieve_home():
        return 'Welcome to Alleb Casting Agency!'

    # Movie Endpoints.

    # Get all available movies.
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(jwt):
        try:
            movies = Movie.query.order_by(Movie.release_date).all()

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies],
                'total_movies': len(movies)
            }), 200
        except BaseException:
            abort(500)

    # Get a movie by movie id.
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movie_by_id(jwt, movie_id):

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    # Add a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(jwt):
        body = request.get_json()

        new_title = body.get('title')
        new_release_date = body.get('release_date')

        if validate_movie(new_title, new_release_date) is False:
            abort(400)

        try:
            movie = Movie(
                title=new_title,
                release_date=new_release_date
            )

            movie.insert()

            movies = Movie.query.order_by(Movie.release_date).all()

            return jsonify({
                'success': True,
                'message': 'movie successfully added',
                'movies': [movie.format() for movie in movies]
            })
        except BaseException:
            abort(422)

    # Update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(jwt, movie_id):
        body = request.get_json()

        edited_title = body.get('title')
        edited_release_date = body.get('release_date')

        if validate_movie(edited_title, edited_release_date) is False:
            abort(400)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.title = edited_title
            movie.release_date = edited_release_date
            movie.update()

            return jsonify({
                'success': True,
                'message': 'movie successfully updated',
                'movie': movie.format()
            })
        except BaseException:
            abort(422)

    # Delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': [movie.format() for movie in movies],
                'total_movies': len(movies)
            }), 200
        except BaseException:
            abort(422)

    # Actor Endpoints

    # Get all available actors.
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(jwt):
        try:
            actors = Actor.query.order_by(Actor.name).all()

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors],
                'total_actors': len(actors)
            }), 200
        except BaseException:
            abort(500)

    # Get a actor by actor id.
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actor_by_id(jwt, actor_id):

        actor = Actor.query.get(actor_id)
        print(actor)
        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

    # Add a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(jwt):
        body = request.get_json()

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        if validate_actor(new_name, new_age, new_gender) is False:
            abort(400)

        try:
            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender
            )

            actor.insert()

            actors = Actor.query.order_by(Actor.name).all()

            return jsonify({
                'success': True,
                'message': 'actor successfully added',
                'actors': [actor.format() for actor in actors]
            })
        except BaseException:
            abort(422)

    # Update a actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(jwt, actor_id):
        body = request.get_json()

        edited_name = body.get('name')
        edited_age = body.get('age')
        edited_gender = body.get('gender')

        if validate_actor(edited_name, edited_age, edited_gender) is False:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.name = edited_name
            actor.age = edited_age
            actor.gender = edited_gender
            actor.update()

            return jsonify({
                'success': True,
                'message': 'actor successfully updated',
                'actor': actor.format()
            })
        except BaseException:
            abort(422)

    # Delete an actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            actors = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': [actor.format() for actor in actors],
                'total_actors': len(actors)
            }), 200
        except BaseException:
            abort(422)

    # Error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized",
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(err):
        return jsonify(
            err.error
        ), err.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
