import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movies, Actors, setup_db


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_actor(self):
        payload = {
            'name': 'James Bond',
            'age': 33,
            'gender': 'female'
        }
        response = self.client().post('/actors', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor created')

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_edit_actor(self):
        payload = {'name': 'James Blonder'}
        response = self.client().patch('/actors/1', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # def test_delete_actor(self):
    #     response = self.client().delete('/actors/1')
    #     data = json.loads(response.data)
    #     actor = Actors.query.filter(Actors.id == 1).one_or_none()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)

    def test_create_movie(self):
        payload = {
            'title': 'Agent 47',
            'release_date': '2020-2-2'
        }
        response = self.client().post('/movies', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie created')

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_edit_movie(self):
        payload = {'title': 'Princess Pride'}
        response = self.client().patch('/movies/2', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        response = self.client().delete('/movies/1')
        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/29')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_422(self):
        payload = {
            'title': '',
            'release_date': 2020
        }
        res = self.client().post('/movies', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_400(self):
        payload = {'title': ''}
        res = self.client().post('/movies', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# dropdb casting_agency_test && createdb casting_agency_test
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
