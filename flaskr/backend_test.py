from flaskr.backend import Backend

# TODO(Project 1): Write tests for Backend methods.
import unittest
from unittest.mock import MagicMock, patch
import hashlib

class TestBackend(unittest.TestCase):

    @patch('backend.google.cloud.storage.Client')
    def test_init(self, mock_storage_client):
        bucket_name = 'test-bucket'
        backend = Backend(bucket_name)
        self.assertEqual(backend.bucket.name, bucket_name)

    @patch('backend.google.cloud.storage.Bucket.get_blob')
    def test_get_wiki_page(self, mock_get_blob):
        name = 'test-page'
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = 'This is a test wiki page'
        mock_get_blob.return_value = mock_blob
        backend = Backend('test-bucket')
        page = backend.get_wiki_page(name)
        self.assertEqual(page, 'This is a test wiki page')

    @patch('backend.google.cloud.storage.Bucket.list_blobs')
    def test_get_all_page_names(self, mock_list_blobs):
        mock_blob1 = MagicMock()
        mock_blob1.name = 'pages/test-page1'
        mock_blob2 = MagicMock()
        mock_blob2.name = 'pages/test-page2'
        mock_list_blobs.return_value = [mock_blob1, mock_blob2]
        backend = Backend('test-bucket')
        pages = backend.get_all_page_names()
        self.assertEqual(pages, ['test-page1', 'test-page2'])

    @patch('backend.google.cloud.storage.Bucket.blob')
    def test_upload(self, mock_blob):
        data = 'This is a test file'
        filename = 'test-file.txt'
        backend = Backend('test-bucket')
        backend.upload(data, filename)
        mock_blob.assert_called_with(f"uploads/{filename}")
        mock_blob.return_value.upload_from_string.assert_called_with(data)

    @patch('backend.hashlib.sha256')
    @patch('backend.google.cloud.storage.Bucket.blob')
    def test_sign_up(self, mock_blob, mock_sha256):
        username = 'test-user'
        password = 'test-password'
        hashed_password = 'a4e4f3b93353e1af2c9b8418b5d5e11d0d4e4c0b8e4b1d46f834df433beaa9c9'
        mock_blob.return_value.exists.return_value = False
        mock_sha256.return_value.hexdigest.return_value = hashed_password
        backend = Backend('test-bucket')
        result = backend.sign_up(username, password)
        mock_blob.assert_called_with(f"users/{username}")
        mock_blob.return_value.upload_from_string.assert_called_with(hashed_password)
        self.assertTrue(result)

        # Test that signing up with an existing username returns False
        mock_blob.return_value.exists.return_value = True
        result = backend.sign_up(username, password)
        self.assertFalse(result)

    @patch('backend.google.cloud.storage.Bucket.get_blob')
    def test_sign_in(self, mock_get_blob):
        username = 'test-user'
        password = 'test-password'
        hashed_password = 'a4e4f3b93353e1af2c9b8418b5d5e11d0d4e4c0b8e4b1d46f834df433beaa9c9'
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = hashed_password
        mock_get_blob.return_value = mock_blob
        backend = Backend('test-bucket')

        # Test logging in with correct username and password
        result = backend.sign_in(username, password)
        self.assertTrue(result)

        # Test logging
    def test_sign_up_already_existing_user(self, mock_client, mock_bucket):
        # Test signing up an already existing user
        backend = Backend("test-bucket")
        username = "existing_user"
        password = "password"
        # Set up mock bucket to simulate an already existing user
        mock_blob = mock.MagicMock()
        mock_blob.exists.return_value = True
        mock_bucket.get_blob.return_value = mock_blob
        result = backend.sign_up(username, password)
        assert result == False


    def test_sign_in_correct_password(self, mock_client, mock_bucket):
        # Test signing in with correct password
        backend = Backend("test-bucket")
        username = "user1"
        password = "password"
        # Set up mock bucket to simulate a user with a hashed password
        hashed_password = backend._hash_password(password)
        mock_blob = mock.MagicMock()
        mock_blob.download_as_text.return_value = hashed_password
        mock_bucket.get_blob.return_value = mock_blob
        result = backend.sign_in(username, password)
        assert result == True


    def test_sign_in_incorrect_password(self, mock_client, mock_bucket):
        # Test signing in with incorrect password
        backend = Backend("test-bucket")
        username = "user1"
        password = "password"
        # Set up mock bucket to simulate a user with a different hashed password
        hashed_password = backend._hash_password("different_password")
        mock_blob = mock.MagicMock()
        mock_blob.download_as_text.return_value = hashed_password
        mock_bucket.get_blob.return_value = mock_blob
        result = backend.sign_in(username, password)
        assert result == False


    def test_get_image_existing_image(self, mock_client, mock_bucket):
        # Test getting an existing image
        backend = Backend("test-bucket")
        image_name = "test_image.jpg"
        # Set up mock bucket to simulate an existing image
        mock_blob = mock.MagicMock()
        mock_blob.download_as_bytes.return_value = b"test image data"
        mock_bucket.get_blob.return_value = mock_blob
        result = backend.get_image(image_name)
        assert result == b"test image data"


    def test_get_image_non_existing_image(self, mock_client, mock_bucket):
        # Test getting a non-existing image
        backend = Backend("test-bucket")
        image_name = "non_existing_image.jpg"
        # Set up mock bucket to simulate a non-existing image
        mock_bucket.get_blob.return_value = None
        result = backend.get_image(image_name)
        assert result == None


    def test_hash_password(self):
        # Test the _hash_password method
        backend = Backend("test-bucket")
        password = "password"
        hashed_password = backend._hash_password(password)
        assert hashed_password == hashlib.sha256(password.encode()).hexdigest()
