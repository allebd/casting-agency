import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9EVTNNRVkxTlRnME1rWTFPRE00TlVORU9EbEJRakUwTVRoRk1qZzBOa1ZGUkRrelJFVXdRZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWxsZWJkLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNzE1ODkwOTY3NDQzMDQwMjE2MyIsImF1ZCI6WyJjYXN0aW5nIiwiaHR0cHM6Ly9jYXN0aW5nLWFsbGViZC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5NzU1OTQxLCJleHAiOjE1Nzk3NjMxNDEsImF6cCI6InZlbFB3c2RDdWhZbzRrNjdFT003cnBCWUNwY3I1SWpCIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.MP5NaonFUmWGFbys8U8filkLM0O7ISW0j5p8bVekmbd4p5hF97aEWFIMtOuGFDBXFRTfXgfbY23ycA5hVmcECQpCZri80vg73nz2oAJLyyAowFwPXVoGO11bfnS5vT-WDd3F3N71GIV_reLntIrX0xClKUdf7JviI_L6QCUAqwHhu1CvL2SJOFysE7aa6Rdn5QgzN96p0eCwgPqkDCzmBl7lVZjty8-z3Kvrtq9bO3csVF4hUoImekNZk7B17CunR8b279I7CD2F6XZEz1_36LctS3drMEGsNYi8M5L0raanLqfGQbSKw3m0hFMFd0yswVLX7LlAbYxEWp6HHSJp8A'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9EVTNNRVkxTlRnME1rWTFPRE00TlVORU9EbEJRakUwTVRoRk1qZzBOa1ZGUkRrelJFVXdRZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWxsZWJkLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDgwNDExNDQ4NjI4Nzk0OTcxMSIsImF1ZCI6WyJjYXN0aW5nIiwiaHR0cHM6Ly9jYXN0aW5nLWFsbGViZC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5NzU2MTAxLCJleHAiOjE1Nzk3NjMzMDEsImF6cCI6InZlbFB3c2RDdWhZbzRrNjdFT003cnBCWUNwY3I1SWpCIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.H24Nx73LYsO9oWBrYZX3g6bW2cUKAEKh8oQKL8JTMuaOUuqfCRqXpzG7Af7EvoT5ELAIALRJ2Pm5GNISHmCXOh3ZGEgjpDIp6fSOPjENRCfDM5qidI2xs24MMJXzPFMz319EYgvbC_6lPfolXEcYpVDLbdPt_uSfsgk8pB4e_chPRI5jrs4HRfRH0K_N5sBRGlrb-c8bAvKsksX0OkG7T4Sf8PrsfzrVcP2GHOkKB-9h4rLVLLpq_LuriVPhD5Vb0sQA2b94mgE6j5a1RqDyWaLuLQAzMOpzkheEmfeOd4I6xBr5EYD1TJ2tqEMp3WkmK-_zNSW3MkRlBQhzTZRbDA'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9EVTNNRVkxTlRnME1rWTFPRE00TlVORU9EbEJRakUwTVRoRk1qZzBOa1ZGUkRrelJFVXdRZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWxsZWJkLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTM2NDQ4NTU4MTcxMDU4OTA2NCIsImF1ZCI6WyJjYXN0aW5nIiwiaHR0cHM6Ly9jYXN0aW5nLWFsbGViZC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5NzU2MjI2LCJleHAiOjE1Nzk3NjM0MjYsImF6cCI6InZlbFB3c2RDdWhZbzRrNjdFT003cnBCWUNwY3I1SWpCIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Jcqk95933DkQFtiP7dHRB1QXI3n_KcArvPUFv4WIUcFrEFq62hjpmiXgMj2bchPk66gA0PSvZLpO8KX6eTdT5E8ZQ72Hb6PRNi1gu9CR0ECjQcARyMRkh_Crr0_7lrXFaASstvsv0MCLxGev7ywHe7cWzQX5CBPGvtyOL9OWvSa3HJyUZsuKSGwRsPwH2F41I6LWMlAP0FPrYaAfK5JjKVTGKdtU6aXQo8O8qwOwjfruTFQwyEZHeoO9J1fa8lvJEHOr-BG6Wv9MkQjq3Zz3KlOWt7_inUxhp4nLntrJ2pQeMkXrqpAfv2_QvZd7lXTyZzor4ssF3kCxaCwoJLbcRg'


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

        self.new_actor = {
            'name': 'Tom Cruise',
            'age': 57,
            'gender': 'male'
        }

        self.empty_actor = {
            'name': '',
            'age': 45,
            'gender': ''
        }

        self.update_actor = {
            'name': 'Will Smith',
            'age': 51,
            'gender': 'male'
        }

        self.producer_permission = {
            'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER
        }

        self.director_permission = {
            'Authorization': 'Bearer ' + CASTING_DIRECTOR
        }

        self.assistant_permission = {
            'Authorization': 'Bearer ' + CASTING_ASSISTANT
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

    #----------------------------------------------------------------------------#
    # Movie Endpoint Test.
    #----------------------------------------------------------------------------#

    # Get all movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    # Get a movie by movie id
    def test_get_movies_by_id(self):
        res = self.client().get('/movies/1', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_404_invalid_get_movies_by_id(self):
        res = self.client().get('/movies/1000', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Create a movie
    def test_create_new_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'movie successfully added')
        self.assertTrue(len(data['movies']))

    def test_400_if_movie_field_empty(self):
        res = self.client().post(
            '/movies',
            json=self.empty_movie,
            headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_401_if_create_movie_unauthorized(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.assistant_permission)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    # Update a movie
    def test_update_movie(self):
        res = self.client().patch(
            '/movies/3',
            json=self.update_movie,
            headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'movie successfully updated')
        self.assertTrue(len(data['movie']))

    def test_400_if_update_movie_field_empty(self):
        res = self.client().patch(
            '/movies/3',
            json=self.empty_movie,
            headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_if_invalid_update_movie(self):
        res = self.client().patch(
            '/movies/1000',
            json=self.update_movie,
            headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Delete a movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=self.producer_permission)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_401_if_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/1', headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    #----------------------------------------------------------------------------#
    # Actor Endpoints Test.
    #----------------------------------------------------------------------------#

    # Get all actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    # Get an actor by action id
    def test_get_actors_by_id(self):
        res = self.client().get('/actors/1', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_404_invalid_get_actors_by_id(self):
        res = self.client().get('/actors/1000', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Create an actor
    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'actor successfully added')
        self.assertTrue(len(data['actors']))

    def test_400_if_actor_field_empty(self):
        res = self.client().post(
            '/actors',
            json=self.empty_actor,
            headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Update an actor
    def test_update_actor(self):
        res = self.client().patch(
            '/actors/3',
            json=self.update_actor,
            headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'actor successfully updated')
        self.assertTrue(len(data['actor']))

    def test_400_if_update_actor_field_empty(self):
        res = self.client().patch(
            '/actors/3',
            json=self.empty_actor,
            headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_if_invalid_update_actor(self):
        res = self.client().patch(
            '/actors/1000',
            json=self.update_actor,
            headers=self.producer_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_401_if_update_actor_unauthorized(self):
        res = self.client().patch(
            '/actors/3',
            json=self.update_actor,
            headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    # Delete an actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers=self.director_permission)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.director_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_401_if_delete_actor_unauthorized(self):
        res = self.client().delete('/actors/3', headers=self.assistant_permission)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')


# dropdb casting_test && createdb casting_test


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
