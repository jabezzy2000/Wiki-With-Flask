from flaskr import create_app
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, url_for
from flaskr.backend import Backend
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"This project is owned by Jabez, Donald and Ivan.\n" in resp.data


# def test_pages_index(client):
#     with patch('flaskr.backend.Backend.get_all_page_names') as mock_backend:
#         mock_backend.return_value = ['page1', 'page2']
#         response = client.get('/pages')
#         assertEqual(response.status_code, 200)
#         assertIn(b'page1', response.data)
#         assertIn(b'page2', response.data)


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"This project is owned by Jabez, Donald and Ivan.\n", resp.data)

    def test_pages_index(self):
        with patch('flaskr.backend.Backend.get_all_page_names') as mock_backend:
            mock_backend.return_value = ['page1', 'page2']
            response = self.client.get('/pages')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'page1', response.data)
            self.assertIn(b'page2', response.data)


# @patch.object(Backend, 'sign_up')
# def test_signup_success(mock_sign_up):
#     mock_sign_up.return_value = True
#     response = client.post('/signup', data=dict(
#         username='test_user',
#         password='test_password'
#     ), follow_redirects=True)
#     assert(response)
#     assertIn(b'Successfully signed up!', response.data)
# TODO(Project 1): Write tests for other routes.