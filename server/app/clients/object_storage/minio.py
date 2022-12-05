from bulkboto3 import BulkBoto3, StorageTransferPath
import os

class MinIOStorage:
    def __init__(self, key, secret, bucket) -> None:
        self.key = key
        self.secret = secret
        self.bucket = bucket

        self.NUM_TRANSFER_THREADS = 10
        self.TRANSFER_VERBOSITY = True

        self.bulkboto_agent = BulkBoto3(
            resource_type="s3",
            endpoint_url="http://127.0.0.1:9000",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            max_pool_connections=300,
            verbose=self.TRANSFER_VERBOSITY,
        )

        self._create_bucket(bucket)

    def _create_bucket(self, name):
        try:
            self.bulkboto_agent.create_new_bucket(bucket_name=name)
            return True
        except Exception as e:
            print(e)
            return False
    
    def put(self, key, obj):
        try:
            local = os.path.abspath(obj.name)
            remote = key
            self.bulkboto_agent.upload(
                bucket_name=self.bucket,
                upload_paths=[StorageTransferPath(local, remote)]
            )
            return {"status": "success", "path": remote}
        except Exception as e:
            print(e)
            return None
    
    def get(self, key):
        try:
            local = "bucket/tasks/" + str(key)
            remote = key
            self.bulkboto_agent.download(
                bucket_name=self.bucket,
                download_paths=[StorageTransferPath(local, remote)]
            )
            filepath = os.path.abspath(os.path.expanduser(local))
            with open(filepath, "r") as file:
                return file.readlines()
        except Exception as e:
            print(e)
            return []
