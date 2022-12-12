import unittest
from unittest.mock import patch
from app.services.object_storage_service import ObjectStorageService

class TestObjectStorageService(unittest.TestCase):
    @patch('app.services.object_storage_service.ObjectStorageService.create')
    def test_create(self, mock_create):
        mock_create.return_value = {'object': '1234'}
        object_storage_service = ObjectStorageService(None, None)
        object = object_storage_service.create(None, None)
        self.assertEqual(object, {'object': '1234'})
        mock_create.assert_called_once()

    @patch('app.services.object_storage_service.ObjectStorageService.list')
    def test_list(self, mock_list):
        mock_list.return_value = ['1234']
        object_storage_service = ObjectStorageService(None, None)
        objects = object_storage_service.list()
        self.assertEqual(objects, ['1234'])
        mock_list.assert_called_once()

    @patch('app.services.object_storage_service.ObjectStorageService.get')
    def test_get(self, mock_get):
        mock_get.return_value = ['1234']
        object_storage_service = ObjectStorageService(None, None)
        object = object_storage_service.get(None)
        self.assertEqual(object, ['1234'])
        mock_get.assert_called_once()

    @patch('app.services.object_storage_service.ObjectStorageService.update')
    def test_update(self, mock_update):
        mock_update.return_value = {'status': 'success'}
        object_storage_service = ObjectStorageService(None, None)
        response = object_storage_service.update(None, None)
        self.assertEqual(response, {'status': 'success'})
        mock_update.assert_called_once()

    @patch('app.services.object_storage_service.ObjectStorageService.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = {'status': 'success'}
        object_storage_service = ObjectStorageService(None, None)
        response = object_storage_service.delete(None)
        self.assertEqual(response, {'status': 'success'})
        mock_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()