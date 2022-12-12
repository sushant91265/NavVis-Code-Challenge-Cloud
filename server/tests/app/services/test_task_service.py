import unittest
from unittest.mock import patch
from server.app.services.task_service import TaskService
from app.dto.models import Task, TaskCollection, TaskResultCollection

class TestTaskService(unittest.TestCase):
    @patch('app.services.object_storage_service.ObjectStorageService.put')
    @patch('app.services.metadata_service.MetadataService.save_task')
    def test_create(self, mock_put, mock_save_task):
        mock_put.return_value = {'status': 'success', 'path': '1234'}
        mock_save_task = {'status': 'success'}
        task_service = TaskService(None, None)
        task = task_service.create(None, None)
        response = Task(task_id='1234', path='1234')
        self.assertEqual(task, response)
        mock_put.assert_called_once()
        mock_save_task.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.get_tasks')
    def test_list(self, mock_get_tasks):
        mock_get_tasks.return_value = ['1234']
        task_service = TaskService(None, None)
        taskCollection = TaskCollection(items=['1234'])
        tasks = task_service.list()
        self.assertEqual(tasks, taskCollection)
        mock_get_tasks.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.get_results')
    def test_get_results(self, mock_get_results):
        mock_get_results.return_value = ['1234']
        task_service = TaskService(None, None)
        taskResultCollection = TaskResultCollection(items=['1234'])
        results = task_service.get_results(4)
        self.assertEqual(results, taskResultCollection)
        mock_get_results.assert_called_once()

    @patch('app.services.metadata_service.MetadataService.delete')
    def test_delete_results(self, mock_delete):
        mock_delete.return_value = ['1234']
        task_service = TaskService(None, None)
        results = task_service.delete_results(4)
        self.assertEqual(results, 4)
        mock_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()