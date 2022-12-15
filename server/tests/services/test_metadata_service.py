import unittest
from unittest.mock import patch
from app.services.metadata_service import MetadataService

class TestMetadataService(unittest.TestCase):
    def setUp(self):
        self.client = MetadataService(None)
        self.key = "test"
        
    @patch('app.services.metadata_service.MetadataService.save_task')
    def test_save_task(self, mock_save_task):
        self.client.save_task(self.key)
        mock_save_task.assert_called_once_with(self.key)
    
    @patch('app.services.metadata_service.MetadataService.get_tasks')
    def test_get_tasks(self, mock_get_tasks):
        self.client.get_tasks()
        mock_get_tasks.assert_called_once_with()
    
    @patch('app.services.metadata_service.MetadataService.get_results')
    def test_get_results(self, mock_get_results):
        self.client.get_results(self.key)
        mock_get_results.assert_called_once_with(self.key)
    
    @patch('app.services.metadata_service.MetadataService.delete')
    def test_delete(self, mock_delete):
        self.client.delete(self.key)
        mock_delete.assert_called_once_with(self.key)

if __name__ == '__main__':
    unittest.main()