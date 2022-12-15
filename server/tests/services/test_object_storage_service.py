import unittest
from unittest.mock import patch
from app.services.object_storage_service import ObjectStorageService

class TestObjectStorageService(unittest.TestCase):
    def setUp(self):
        self.client = ObjectStorageService(None)
    
    def test_put(self):
        self.client.client = MockClient()
        response = self.client.put("key", "obj")
        self.assertEqual(response, "put")

    def test_get(self):
        self.client.client = MockClient()
        response = self.client.get("key")
        self.assertEqual(response, "get")

    def test_delete(self):
        self.client.client = MockClient()
        response = self.client.delete("key")
        self.assertEqual(response, "delete")

class MockClient:
    def put(self, key, obj):
        return "put"
    
    def get(self, key):
        return "get"
    
    def delete(self, key):
        return "delete"
    
if __name__ == '__main__':
    unittest.main()
    