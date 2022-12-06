import os
import shutil
from minio import Minio


class MinIOStorage:
    def __init__(self, key, secret, bucket, endpoint="http://localhost:9000"):
        self.key = key
        self.secret = secret
        self.client = Minio(endpoint, key, secret, secure=False)
        self.bucket = bucket

        if self.client.bucket_exists(self.bucket):
            print(f"{self.bucket} already exists")
        else:
            print(f"{self.bucket} does not exist. Creating ...")
            self.client.make_bucket(bucket_name=self.bucket)

    def get(self, key):
        try:
            temp_file = key  
            self.client.fget_object(self.bucket, key, temp_file)
            data = []

            path = os.path.abspath(temp_file)
            print("Downloaded file to " + path)
            with open(path, "r") as file:
                data = file.readlines()
            os.remove(path)
            return data
        except Exception as e:
            print("Error while getting object " + str(key) + " Error " + str(e))
            raise e

    def put(self, key, file):
        try:
            path = os.path.abspath(file.name)
            self.client.fput_object(self.bucket, key, path)
            return {"status": "success", "path": key}
        except Exception as e:
            print("Error while pushing the object for key " + key + " Error: " + str(e))
            return {"status": "failed", "msg": str(e)}
