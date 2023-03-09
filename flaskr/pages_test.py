from flaskr import create_app
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, url_for
from flaskr.backend import Backend
from io import BytesIO
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

    def test_about_page(self):
        with patch('flaskr.backend.Backend.get_image') as mock_backend:
            mock_backend.return_value = b'fake image data'
            resp = self.client.get("/about")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'fake image data', resp.data)

    def test_page_details(self):
        with patch('flaskr.backend.Backend.get_wiki_page') as mock_content:
            mock_content.return_value = "This is the content of the page"
            response = self.client.get('/pages/test_page')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Page', response.data)
            self.assertIn(b'This is the content of the page', response.data)


    def test_upload_file(self):
        with patch('flaskr.backend.Backend.upload') as mock_upload:
            mock_upload.return_value = True
            response = self.client.post('/upload', data=dict(
                file=(BytesIO(b'my file contents'), 'test_file.txt')
            ))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File uploaded successfully!', response.data)

    def test_login(self):
        with patch('flaskr.backend.Backend.sign_in') as mock_verify:
            mock_verify.return_value = True
            response = self.client.post('/login', data=dict(
                username='test_user',
                password='test_password'
            ))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], 'http://localhost/')

    def test_signup(self):
        with patch('flaskr.backend.Backend.sign_up') as mock_create:
            mock_create.return_value = True
            response = self.client.post('/signup', data=dict(
                username='test_user',
                password='test_password'
            ))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers['Location'], 'http://localhost/login')

    def test_logout(self):
        with patch('flaskr.backend.Backend.sign_in') as mock_verify:
            mock_verify.return_value = True
            with patch('flaskr.backend.Backend.logout_user') as mock_logout:
                mock_logout.return_value = True
                response = self.client.get('/logout')
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers['Location'], 'http://localhost/')


# TODO(Project 1): Write tests for other routes.