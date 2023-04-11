# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from google.cloud.exceptions import NotFound, Forbidden, Conflict
from base64 import b64encode
import hashlib
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dijproject-d5a5f3cc6a38.json"


class Backend:

    # Constructor that takes bucket_name as input
    def __init__(self, bucket_name):
        self.client = storage.Client()  # Create a client instance
        self.bucket = self.client.bucket(bucket_name)  # Get a bucket reference

    # Method to get the contents of a wiki page with the given name
    def get_wiki_page(self, name):
        blob = self.bucket.get_blob(
            f"uploads/{name}")  # Get the blob object from the bucket
        if blob is None:  # If the blob object does not exist
            return None  # Return None
        local_file_path = "/tmp/" + name  # Set the local file path for the blob object
        blob.download_to_filename(
            local_file_path)  # Download the blob object to the local file path
        with open(local_file_path,
                  "r") as f:  # Open the local file in read mode
            contents = f.read()  # Read the contents of the file
        return contents  # Return the contents

    # Method to get the names of all wiki pages in the bucket
    def get_all_page_names(self):
        pages = self.bucket.list_blobs(
            prefix="uploads/")  # Get a list of all blobs with prefix "uploads/"
        length = len("uploads/")  # Get the length of the prefix "uploads/"
        return [page.name[length:] for page in pages
               ]  # Return a list of page names by slicing the names of blobs

    # Method to upload a file to the bucket
    def upload(self, filepath, filename):
        try:
            blob = self.bucket.blob(f"uploads/{filename}")
            blob.upload_from_filename(filepath, content_type='text/html')
            return True, "Upload successful"
        except NotFound:
            return False, "Bucket not found"
        except Forbidden:
            return False, "Access to bucket denied"
        except Conflict:
            return False, "A file with the same name already exists in the bucket"
        except Exception as e:
            return False, f"An error occurred during upload: {e}"

    # Method to sign up a user with the given username and password
    def sign_up(self, username, password):
        blob = self.bucket.blob(
            f"users/{username}")  # Get the blob object reference for the user
        if blob.exists():  # If the user already exists
            return False  # Return False
        hashed_pass = self._hash_password(
            password)  # Hash the password using SHA256
        blob.upload_from_string(
            hashed_pass)  # Upload the hashed password to the blob object
        return True  # Return True

    # Method to sign in a user with the given username and password
    def sign_in(self, username, password):
        blob = self.bucket.get_blob(
            f"users/{username}")  # Get the blob object reference for the user
        if blob is None:  # If the user does not exist
            return False  # Return False
        hashed_password = blob.download_as_text().strip(
        )  # Get the hashed password from the blob object
        if hashed_password == self._hash_password(
                password):  # If the input password matches the hashed password
            return True  # Return True
        else:
            return False  # Return False

    def get_image(self, name_of_image):
        """Gets a publicly accessible URL for an image file in the bucket.

        Args:
            name_of_image (str): The name of the image file to get.

        Returns:
            str: A publicly accessible URL for the image file, or None if the file does not exist.

        """
        blob = self.bucket.get_blob(f"/{name_of_image}")
        if blob is None:
            return None
        else:
            return blob.public_url

    def _hash_password(self, password):
        """Hashes a password using SHA-256.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.

        """
        return hashlib.sha256(password.encode()).hexdigest()
