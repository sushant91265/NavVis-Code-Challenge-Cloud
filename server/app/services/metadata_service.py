import app.dto.models
from db.models import Task, Result
from app.dto.models import TaskResult


class MetadataService:
    def __init__(self, db):
        self.db = db

    def save_task(self, task: app.dto.models.Task):
        print("Saving task")
        _task = Task(task_id=task.id, filename=task.filename)
        with self.db.session.begin():
            self.db.session.add(_task)
            self.db.session.commit()
        return {"status": "success", "task": _task}

    def get_tasks(self):
        return self.db.session.query(Task).all()

    def get_results(self, task_id):
        print("Getting results")
        result = (
            self.db.session.query(Result).join(Task).filter(Task.task_id == task_id)
        )
        arr = [row for row in result]
        return arr
    
    def delete(self, task_id):
        print("Deleting results for task " + str(task_id))
        with self.db.session.begin():
            if not self.is_task_id_exists(task_id):
                return {"status": "failure", "reason": "Task not found"}

            results = self.db.session.query(Task).filter(Task.task_id == task_id)
            print("Results: " + str(results))
            arr = [row for row in results]
            if len(arr) == 1:
                id = arr[0].id
                print("Existing id of task " + str(id))
                self.db.session.query(Result).filter(Result.task_id == str(id)).delete()
                self.db.session.commit()
            return {"status": "success"}

    def is_task_id_exists(self, task_id):
        return self.db.session.query(Task).filter(Task.task_id == task_id).count() > 0