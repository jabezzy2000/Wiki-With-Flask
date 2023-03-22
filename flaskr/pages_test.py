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


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        # Check if the home page is loaded successfully by checking the response status code
        # and the presence of a specific string in the response data.
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"This project is owned by Jabez, Donald and Ivan.\n",
                      resp.data)

    def test_pages_index(self):
        # Check if the page index is loaded successfully by mocking the get_all_page_names() function
        # and checking the response status code and the presence of the expected page names in the response data.
        with patch('flaskr.backend.Backend.get_all_page_names') as mock_backend:
            mock_backend.return_value = ['page1', 'page2']
            response = self.client.get('/pages')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'page1', response.data)
            self.assertIn(b'page2', response.data)

    def test_about_page(self):
        # Check if the about page is loaded successfully by mocking the get_image() function
        # and checking the response status code and the presence of the expected image data in the response data.
        with patch('flaskr.backend.Backend.get_image') as mock_backend:
            mock_backend.return_value = b'fake image data'
            resp = self.client.get("/about")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'fake image data', resp.data)

    def test_page_details(self):
        # Check if a specific page is loaded successfully by mocking the get_wiki_page() function
        # and checking the response status code and the presence of the expected page contents in the response data.
        with patch('flaskr.backend.Backend.get_wiki_page') as mock_content:
            mock_content.return_value = "Test file contents"
            response = self.client.get('/pages/testfile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test file contents', response.data)

    def test_upload_file(self):
        # Check if a file is uploaded successfully by mocking the upload() function
        # and checking the response status code and the presence of the expected success message in the response data.
        with patch('flaskr.backend.Backend.upload') as mock_upload:
            mock_upload.return_value = True
            response = self.client.post(
                '/upload',
                data=dict(html_file=(BytesIO(b'my file contents'),
                                     'test_file.txt')))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test_file.txt has been uploaded successfully!',
                          response.data)

    def test_login(self):
        # Use a mock to simulate sign-in
        with patch('flaskr.backend.Backend.sign_in') as mock_verify:
            # Set the mock to return True to simulate a successful sign-in
            mock_verify.return_value = True
            # Send a POST request with the login information
            response = self.client.post('/login',
                                        data=dict(username='test_user',
                                                  password='test_password'))
            # Check that the response has a redirect status code
            self.assertEqual(response.status_code, 302)
            # Check that the response redirects to the home page
            self.assertEqual(response.headers['Location'], 'http://localhost/')

    def test_signup(self):
        # Use a mock to simulate user creation
        with patch('flaskr.backend.Backend.sign_up') as mock_create:
            # Set the mock to return True to simulate successful user creation
            mock_create.return_value = True
            # Send a POST request with the signup information
            response = self.client.post('/signup',
                                        data=dict(username='test_user',
                                                  password='test_password'))
            # Check that the response has a redirect status code
            self.assertEqual(response.status_code, 302)
            # Check that the response redirects to the login page
            self.assertEqual(response.headers['Location'],
                             'http://localhost/login')

    def test_logout(self):
        # Use a mock to simulate sign-in
        with patch('flaskr.backend.Backend.sign_in') as mock_verify:
            # Set the mock to return True to simulate a successful sign-in
            mock_verify.return_value = True
            # Use a mock to simulate logout
            with patch('flaskr.backend.Backend.logout_user') as mock_logout:
                # Set the mock to return True to simulate successful logout
                mock_logout.return_value = True
                # Send a GET request to logout
                response = self.client.get('/logout')
                # Check that the response has a redirect status code
                self.assertEqual(response.status_code, 302)
                # Check that the response redirects to the home page
                self.assertEqual(response.headers['Location'],
                                 'http://localhost/')


            #testing unitttest
