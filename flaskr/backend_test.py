from flaskr.backend import Backend
import os
# TODO(Project 1): Write tests for Backend methods.
import unittest
from unittest.mock import MagicMock, patch
import hashlib


class TestBackend(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.backend = Backend(bucket_name="test-bucket")

    def test_upload_and_get_wiki_page(self):
        # Test uploading a file and retrieving it
        file_contents = "Test file contents"
        file_name = "testfile.html"
        filepath = "/tmp/" + file_name
        with open(filepath, "w") as f:
            f.write(file_contents)
        self.backend.upload(filepath, file_name)
        retrieved_file_contents = self.backend.get_wiki_page(name=file_name)
        self.assertEqual(retrieved_file_contents, file_contents)

    # def test_upload_and_get_wiki_page(self):
    #     # Test uploading a file and retrieving it
    #     file_contents = "Test file contents"
    #     file_name = "testfile.html"
    #     self.backend.upload(filepath="/tmp/testfile.html", filename=file_name)
    #     retrieved_file_name = self.backend.get_wiki_page(name=file_name)
    #     with open(f"/home/donaldechefu/dij-project/flaskr/templates/{retrieved_file_name}", "r") as f:
    #         contents = f.read()
    #     self.assertEqual(contents, file_contents)

    def test_get_all_page_names(self):
        # Test getting all page names
        expected_names = ["testfile1.html", "testfile2.html", "testfile3.html"]
        with patch.object(self.backend.bucket, "list_blobs") as mock_list_blobs:
            mock_list_blobs.return_value = [type('blob', (object,), {'name': f"uploads/{name}"}) for name in expected_names]
            page_names = self.backend.get_all_page_names()
        self.assertListEqual(page_names, expected_names)

    def test_sign_up_and_sign_in(self):
        # Test signing up and signing in
        username = "testuser"
        password = "testpassword"
        result = self.backend.sign_up(username=username, password=password)
        self.assertTrue(result)
        result = self.backend.sign_in(username=username, password=password)
        self.assertTrue(result)

    def test_sign_in_with_invalid_username(self):
        # Test signing in with invalid username
        username = "invaliduser"
        password = "testpassword"
        result = self.backend.sign_in(username=username, password=password)
        self.assertFalse(result)

    def test_sign_in_with_invalid_password(self):
        # Test signing in with invalid password
        username = "testuser"
        password = "invalidpassword"
        result = self.backend.sign_in(username=username, password=password)
        self.assertFalse(result)

    def test_get_image(self):
        # Test getting an image URL
        expected_url = "https://example.com/image.jpg"
        image_name = "testimage.jpg"
        with patch.object(self.backend.bucket, "get_blob") as mock_get_blob:
            mock_get_blob.return_value.public_url = expected_url
            url = self.backend.get_image(name_of_image=image_name)
        self.assertEqual(url, expected_url)
