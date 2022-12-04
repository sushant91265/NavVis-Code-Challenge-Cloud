from pydantic import BaseModel


class Result(BaseModel):
    phone_number: str
    task_id: int

    class Config:
        orm_mode = True


class Task(BaseModel):
    file_name: str
    task_id: str

    class Config:
        orm_mode = True
