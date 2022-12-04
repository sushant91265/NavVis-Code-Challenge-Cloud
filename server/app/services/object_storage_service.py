class ObjectStorageService:
    def __init__(self, client):
        self.client = client

    def put(self, key, obj):
        response = self.client.put(key, obj)
        return response

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        return self.client.delete(key)
