import unittest
from unittest.mock import patch
from app.services.object_storage_service import ObjectStorageService

class TestObjectStorageService(unittest.TestCase):
    def setUp(self):
        self.client = ObjectStorageService(None)
        self.key
    
    @patch('app.services.object_storage_service.ObjectStorageService.put')
    def test_put(self, mock_put):
        self.client.put(self.key, None)
        mock_put.assert_called_once_with(self.key, None)
    
    @patch('app.services.object_storage_service.ObjectStorageService.get')
    def test_get(self, mock_get):
        self.client.get(self.key)
        mock_get.assert_called_once_with(self.key)

    @patch('app.services.object_storage_service.ObjectStorageService.delete')
    def test_delete(self, mock_delete):
        self.client.delete(self.key)
        mock_delete.assert_called_once_with(self.key)

if __name__ == '__main__':
    unittest.main()
    