import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor


class CasingAgencyTestCase(unittest.TestCase):
    """This class represents the casing agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'Home Alone',
            'release_date': '2019-12-13'
        }

        self.empty_movie = {
            'title': '',
            'release_date': ''
        }

        self.update_movie = {
            'title': 'Gemini Man',
            'release_date': '2019-10-11'
        }

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_by_id(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_404_invalid_get_movies_by_id(self):
        res = self.client().get('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'movie successfully added')
        self.assertTrue(len(data['movies']))

    def test_400_if_movie_field_empty(self):
        res = self.client().post('/movies', json=self.empty_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_update_movie(self):
        res = self.client().patch('/movies/3', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'movie successfully updated')
        self.assertTrue(len(data['movie']))

    def test_400_if_update_movie_field_empty(self):
        res = self.client().patch('/movies/3', json=self.empty_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_if_invalid_update_movie(self):
        res = self.client().patch('/movies/1000', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')


# dropdb casting_test && createdb casting_test


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
