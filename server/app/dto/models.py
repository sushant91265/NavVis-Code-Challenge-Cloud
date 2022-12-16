class Task:
    def __init__(self, task_id, filename=None) -> None:
        self.task_id = task_id
        self.filename = filename

    def __str__(self):
        return str(self.task_id)


class TaskCollection:
    def __init__(self, items) -> None:
        self.items = items


class TaskResult:
    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number

    def __str__(self):
        return str(self.phone_number)


class TaskResultCollection:
    def __init__(self, items) -> None:
        self.items = items
