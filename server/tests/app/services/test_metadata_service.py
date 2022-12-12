import unittest
from unittest.mock import patch
from app.services.metadata_service import MetadataService

class TestMetadataService(unittest.TestCase):
    @patch('app.services.metadata_service.MetadataService.create')
    def test_create(self, mock_create):
        mock_create.return_value = {'metadata': '1234'}
        metadata_service = MetadataService(None, None)
        metadata = metadata_service.create(None, None)
        self.assertEqual(metadata, {'metadata': '1234'})
        mock_create.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.list')
    def test_list(self, mock_list):
        mock_list.return_value = ['1234']
        metadata_service = MetadataService(None, None)
        metadatas = metadata_service.list()
        self.assertEqual(metadatas, ['1234'])
        mock_list.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.get')
    def test_get(self, mock_get):
        mock_get.return_value = ['1234']
        metadata_service = MetadataService(None, None)
        metadata = metadata_service.get(None)
        self.assertEqual(metadata, ['1234'])
        mock_get.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.update')
    def test_update(self, mock_update):
        mock_update.return_value = {'status': 'success'}
        metadata_service = MetadataService(None, None)
        response = metadata_service.update(None, None)
        self.assertEqual(response, {'status': 'success'})
        mock_update.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = {'status': 'success'}
        metadata_service = MetadataService(None, None)
        response = metadata_service.delete(None)
        self.assertEqual(response, {'status': 'success'})
        mock_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()