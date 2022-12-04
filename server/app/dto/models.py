class Task:
    def __init__(self, id, filename) -> None:
        self.id = id
        self.filename = filename

    def __str__(self):
        return str(self.id)


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
