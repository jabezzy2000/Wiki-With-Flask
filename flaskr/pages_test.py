from flaskr import create_app
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, url_for
from flaskr.backend import Backend
from io import BytesIO
from urllib.parse import urlparse
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
            self.assertIn(b'Test file content', response.data)



    def test_get_comments(self):
        pagename = "existing_page"

        with patch('flaskr.backend.Backend.get_wiki_page') as mock_get_wiki_page, \
             patch('flaskr.backend.Backend.get_comments') as mock_get_comments:
            
            mock_get_wiki_page.return_value = "Test file contents"
            mock_get_comments.return_value = [{"username": "testuser", "comment": "test comment"}]

            response = self.client.get(f"/pages/{pagename}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"test comment", response.data)

    def test_post_comment(self):
        pagename = "existing_page"

        with patch('flaskr.backend.Backend.get_wiki_page') as mock_get_wiki_page, \
             patch('flaskr.backend.Backend.add_comment') as mock_add_comment, \
             patch('flaskr.backend.Backend.get_comments') as mock_get_comments:
            
            mock_get_wiki_page.return_value = "Test file contents"
            mock_get_comments.return_value = []

            with self.client.session_transaction() as session:
                session['username'] = "testuser"

            response = self.client.post(f"/pages/{pagename}", data={"comment": "test comment"})
            self.assertEqual(response.status_code, 302)
            mock_add_comment.assert_called_once_with(pagename, "testuser", "test comment")

    def test_upload_file(self):
        # Check if a file is uploaded successfully by mocking the upload() function
        # and checking the response status code and the presence of the expected success message in the response data.
        with patch('flaskr.backend.Backend.upload') as mock_upload:
            mock_upload.return_value = (True, 'File upload was successful!')
            response = self.client.post(
                '/upload',
                data=dict(
                    html_file=(BytesIO(b'my file contents'), 'test_file.txt'),
                    file_name='test_file',
                    category='test_category',
                    author='test_author'
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File upload was successful!', response.data)

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
            self.assertEqual(response.status_code, 200)
            # Check that the user is logged in successfully
            self.assertIn(b'Logged in successfully!', response.data)

    def test_signup(self):
        # Use a mock to simulate user creation
        with patch('flaskr.backend.Backend.sign_up') as mock_create:
            # Set the mock to return True to simulate successful user creation
            mock_create.return_value = True
            # Send a POST request with the signup information
            response = self.client.post('/signup',
                                        data=dict(username='test_user',
                                                email='test_email@example.com',
                                                password='test_password',
                                                confirm_password='test_password'))
            # Check that the response has a success status code
            self.assertEqual(response.status_code, 200)
            # Check that the user is signed up successfully and logged in
            self.assertIn(b'Login Page', response.data)

            # Test for password mismatch
            response = self.client.post('/signup',
                                        data=dict(username='test_user',
                                                email='test_email@example.com',
                                                password='test_password',
                                                confirm_password='wrong_password'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Passwords do not match', response.data)

            # Test for existing username
            mock_create.return_value = False
            response = self.client.post('/signup',
                                        data=dict(username='test_user',
                                                email='test_email@example.com',
                                                password='test_password',
                                                confirm_password='test_password'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Username already exists', response.data)

    def test_search(self):
        # Mock the backend.get_all_page_names() method
        with patch('flaskr.backend.Backend.get_all_page_names') as mock_backend:
            # Define the mock return value
            mock_backend.return_value = [
                'cat1_author1_page1',
                'cat1_author2_page2',
                'cat2_author1_page3',
                'cat2_author2_page4'
            ]

            # Test search with a query
            response = self.client.get('/search', query_string={'q': 'page1'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'cat1_author1_page1', response.data)

            # Test search with a category
            response = self.client.get('/search', query_string={'q': 'page', 'category': 'cat1'})
            print(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'cat1_author2_page2', response.data)
            

            # Test search with an author
            response = self.client.get('/search', query_string={'q': 'page', 'author': 'author1'})
            self.assertEqual(response.status_code, 200)
    
    
    def test_logout(self):
        # Log in the user by setting the session variable
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        # Log out the user by sending a GET request to the logout route
        response = self.client.get('/logout')

        # Check that the response has a redirect status code
        self.assertEqual(response.status_code, 302)

        # Create an application context to use url_for
        with self.app.test_request_context():
            # Check that the response redirects to the login page
            expected_location = urlparse(url_for('login', _external=True)).path
            actual_location = urlparse(response.headers['Location']).path
            self.assertEqual(actual_location, expected_location)

        # Check that the user session is cleared
        with self.client.session_transaction() as session:
            self.assertNotIn('username', session)

