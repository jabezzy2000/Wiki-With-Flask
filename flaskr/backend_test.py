#Import necessary modules
from flaskr.backend import Backend
import os
import unittest
from unittest.mock import MagicMock, patch
import hashlib

#Define a test class for Backend methods


class TestBackend(unittest.TestCase):

    # Set up the Backend instance for testing
    @classmethod
    def setUpClass(cls):
        cls.backend = Backend(bucket_name="dij-test-bucket")

    # Test uploading a file and retrieving it
    def test_upload_and_get_wiki_page(self):
        file_contents = "Test file contents"
        file_name = "testfile.html"
        filepath = "/tmp/" + file_name
        with open(filepath, "w") as f:
            f.write(file_contents)
        self.backend.upload(filepath, file_name)
        retrieved_file_contents = self.backend.get_wiki_page(name=file_name)
        self.assertEqual(retrieved_file_contents, file_contents)

    # Test getting all page names
    def test_get_all_page_names(self):
        expected_names = ["testfile1.html", "testfile2.html", "testfile3.html"]
        with patch.object(self.backend.bucket, "list_blobs") as mock_list_blobs:
            mock_list_blobs.return_value = [
                type('blob', (object,), {'name': f"uploads/{name}"})
                for name in expected_names
            ]
            page_names = self.backend.get_all_page_names()
        self.assertListEqual(page_names, expected_names)

    # Test signing up and signing in
    def test_sign_up_and_sign_in(self):
        username = "testuser"
        password = "testpassword"
        result = self.backend.sign_up(username=username, password=password)
        self.assertFalse(result)
        result = self.backend.sign_in(username=username, password=password)
        self.assertTrue(result)

    # Test signing in with invalid username
    def test_sign_in_with_invalid_username(self):
        username = "invaliduser"
        password = "testpassword"
        result = self.backend.sign_in(username=username, password=password)
        self.assertFalse(result)

    # Test signing in with invalid password
    def test_sign_in_with_invalid_password(self):
        username = "testuser"
        password = "invalidpassword"
        result = self.backend.sign_in(username=username, password=password)
        self.assertFalse(result)

    # Test getting an image URL
    def test_get_image(self):
        expected_url = "https://example.com/image.jpg"
        image_name = "testimage.jpg"
        with patch.object(self.backend.bucket, "get_blob") as mock_get_blob:
            mock_get_blob.return_value.public_url = expected_url
            url = self.backend.get_image(name_of_image=image_name)
        self.assertEqual(url, expected_url)

#random comment
