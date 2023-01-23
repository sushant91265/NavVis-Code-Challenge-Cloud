import unittest
from unittest.mock import patch, MagicMock
from app.services.task_service import TaskService
from app.dto.models import Task, TaskCollection, TaskResult, TaskResultCollection
from app.utils.util import get_uuid

class TestTaskService(unittest.TestCase):
    
    def test_get_results(self):
        task_service = TaskService(None, MockMetadaService()) 
        task_results = TaskResult(phone_number='1234')
        taskResultCollection = TaskResultCollection(items=[task_results])

        results = task_service.get_results(4)
        self.assertEqual(len(results.items), len(taskResultCollection.items))
        for result, expected_result in zip(results.items, taskResultCollection.items):
            self.assertEqual(result.phone_number, expected_result.phone_number)
    
    @patch('app.services.task_service.TaskService')
    def test_get_results(self, mock_task_service):
        mock_obj = mock_task_service.return_value
        mock_get_results = mock_obj.get_results = MagicMock(return_value=['1234'])
        results = mock_obj.get_results(4)
        mock_get_results.assert_called_once_with(4)
        self.assertEqual(len(results), 1)

    def test_list(self):
        task_service = TaskService(None, MockMetadaService()) 
        task = Task(id=1, filename='test')
        taskCollection = TaskCollection(items=[str(task.id)])

        tasks = task_service.list()
        self.assertEqual(len(tasks.items), len(taskCollection.items))
        for task, expected_task in zip(tasks.items, taskCollection.items):
            self.assertEqual(task, expected_task)

    def test_delete_results(self):
        task_service = TaskService(None, MockMetadaService()) 
        response = task_service.delete_results(4)
        self.assertEqual(response["status"], "success")

    @patch('app.services.task_service.get_uuid')
    def test_create(self, mock_get_uuid):
        mock_get_uuid.return_value = '1'
        task_service = TaskService(MockObjectStorageService(), MockMetadaService()) 
        task = Task(id='1', filename='test')
        response = task_service.create('test', 'test')
        self.assertEqual(response["task"], str(task))

    def test_is_task_id_exists(self):
        task_service = TaskService(None, MockMetadaService()) 
        self.assertTrue(task_service.is_task_id_exists(4))



class MockObjectStorageService:
    def put(self, file_name, file):
        return {"status": "success", "path": "test"}
    
    def get(self, file_name):
        return {"status": "success", "path": "test"}

    def delete(self, file_name):
        return {"status": "success", "path": "test"}
    

class MockMetadaService:
    def get_results(self, task_id):
        return ['1234']

    def get_tasks(self):
        return [Task(id=1, filename='test')]
    
    def save_task(self, task):
        return {"status": "success", "task": task}

    def delete(self, task_id):
        return {"status": "success"}

    def is_task_id_exists(self, task_id):
        return True


if __name__ == '__main__':
    unittest.main()