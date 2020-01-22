import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, Movie, Actor
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

    # Get all available movies.
    @app.route('/movies', methods=['GET'])
    def retrieve_movies():
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
    def retrieve_movie_by_id(movie_id):
        
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
    def create_movies():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

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
        except BaseException as err:
            print(err)
            abort(422)

    # Update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def edit_movie(movie_id):
        body = request.get_json()

        edited_title = body.get('title', None)
        edited_release_date = body.get('release_date', None)

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
    def delete_question(movie_id):
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

    # Error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
