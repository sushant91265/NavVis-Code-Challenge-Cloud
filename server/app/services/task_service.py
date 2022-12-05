from app.utils.util import get_uuid, get_timestamp_ms
from app.dto.models import Task, TaskCollection, TaskResultCollection, TaskResult


class TaskService:
    def __init__(self, object_storage_service, metadata_service):
        self.object_storage_service = object_storage_service
        self.metadata_service = metadata_service


    def create(self, file, name):
        task_id = get_uuid()
        file_name = name + "_" + str(get_timestamp_ms()) + "_" + task_id[:4]
        response = self.object_storage_service.put(file_name, file)

        print("Uploaded file: " + name)

        if response["status"] != "success":
            return None

        task = Task(task_id, response["path"])
        ms_response = self.metadata_service.save_task(task)
        if ms_response["status"] != "success":
            return None

        print("queued file for processing " + name + " with task id " + task_id)

        return {"task": str(task)}


    def list(self):
        tasks = self.metadata_service.get_tasks()
        return TaskCollection(items=[str(task.task_id) for task in tasks])


    def get_results(self, task_id):
        results = self.metadata_service.get_results(task_id)
        return TaskResultCollection(items=[TaskResult(res.phone_number) for res in results])


    def delete(self, task_id):
        response = self.metadata_service.delete(task_id)
        return response
