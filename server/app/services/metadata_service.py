import app.dto.models
from db.models import Task, Result
from app.dto.models import TaskResult


class MetadataService:
    def __init__(self, db):
        self.db = db

    def save_task(self, task: app.dto.models.Task):
        _task = Task(task_id=task.id, filename=task.filename)
        with self.db.session.begin():
            self.db.session.add(_task)
            self.db.session.commit()
        return {"status": "success", "task": _task}

    def get_tasks(self):
        return self.db.session.query(Task).all()

    def get_results(self, task_id):
        result = (
            self.db.session.query(Result).join(Task).filter(Task.task_id == task_id)
        )
        arr = [row for row in result]
        return arr
