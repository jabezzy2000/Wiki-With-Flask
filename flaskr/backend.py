# TODO(Project 1): Implement Backend according to the requirements.
import google.cloud
import hashlib
class Backend:

    def __init__(self,bucket_name):
        self.client = google.cloud.storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def get_wiki_page(self, name):
        blob = self.bucket.get_blob(f"pages/{name}")
        if blob is None:
            return None
        return blob.download_as_text()

    def get_all_page_names(self):
        pages = self.bucket.list_blobs(prefix="pages/")
        length = len("pages/")
        return [page.name[length:] for page in pages]


    def upload(self,data,filename):
        blob = self.bucket.blob(f"uploads/{filename}")
        blob.upload_from_string(data)
        pass

    def sign_up(self,username,password):
        blob = self.bucket.blob(f"users/{username}")
        if blob.exists():
            return False
        hashed_pass = self._hash_password(password)
        blob.upload_from_string(hashed_pass)
        return True

    def sign_in(self,username,password):
        blob = self.bucket.get_blob(f"users/{username}")
        if blob is None:
            return False
        hashed_password = blob.download_as_text().strip()
        if hashed_password == self._hash_password(password):
            return True
        else:
            return False
        pass

    def get_image(self,name_of_image):
        blob = self.bucket.get_blob(f"images/{name_of_image}")
        if blob is None:
            return None
        else:
            return blob.download_as_bytes()
        pass

    def _hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()
