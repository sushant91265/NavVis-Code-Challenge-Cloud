import time

import uvicorn
import os

from fastapi import FastAPI, UploadFile, File, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from apscheduler.schedulers.background import BlockingScheduler

from app.clients.object_storage.minio import MinIOStorage
from app.services.object_storage_service import ObjectStorageService
from app.services.task_service import TaskService
from app.services.metadata_service import MetadataService
from app.utils.util import write_to_temp_file

from app.jobs.worker import process_tasks


app = FastAPI()
USER = os.getenv("DB_USER", "root")
PASS = os.getenv("DB_PASS", "root")
HOST = os.getenv("DB_HOST", "localhost")
NAME = os.getenv("DB_NAME", "phone_numbers")
DATABASE_URI = f"postgresql://{USER}:{PASS}@{HOST}/{NAME}"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URI)

ACCESS_KEY = os.getenv("access_key", "admins")
ACCESS_SECRET = os.getenv("access_secret", "Strong#Pass#2022")
BUCKET = os.getenv("bucket", "phonenumbers")
ENDPOINT = os.getenv("ENDPOINT","localhost:9000")
minio = MinIOStorage(ACCESS_KEY, ACCESS_SECRET, BUCKET, endpoint=ENDPOINT)

SCHEDULER_TIME = os.getenv("SCHEDULER_TIME", 30)

obj_service = ObjectStorageService(minio)
md_service = MetadataService(db)
task_service = TaskService(obj_service, md_service)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/task/{task_id}/results")
def get_results(task_id: str, response: Response):
    if not task_service.is_task_id_exists(task_id):
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
    return task_service.get_results(task_id)


@app.get("/tasks")
def get_tasks(response: Response):
    task_list = task_service.list()
    if task_list is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
    return task_list


@app.post("/upload")
def upload(response: Response, file: UploadFile = File(...)):
    temp = None
    try:
        temp = write_to_temp_file(file)
        response = task_service.create(temp, file.filename)
        return response
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "There was an error processing the file " + str(e)}
    finally:
        if temp:
            os.remove(temp.name)


@app.delete("/tasks/{task_id}/results")
def delete(task_id: str, response: Response):
    del_response = task_service.delete_results(task_id)
    if del_response.get('status') == "failure":
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


def create_scheduler():
    background_scheduler = BlockingScheduler()
    background_scheduler.add_job(
        process_tasks,
        kwargs={"db": db, "object_storage_service": obj_service},
        trigger="interval",
        seconds=SCHEDULER_TIME,
    )
    return background_scheduler


if __name__ == "__main__":
    scheduler = create_scheduler()
    try:
        if not os.getenv("ASYNC"):
            print("STARTING SERVER")
            uvicorn.run(app, host="0.0.0.0", port=8000)
        else:
            scheduler.start()
            while True:
                time.sleep(SCHEDULER_TIME)
    except Exception as e:
        print(e)
        if scheduler:
            scheduler.shutdown()
    finally:
        print("Shutting down")