import uvicorn
import os
import time

from fastapi import FastAPI, UploadFile, File
from fastapi_sqlalchemy import DBSessionMiddleware, db
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

from app.clients.object_storage.desktop import DesktopOS
from app.services.object_storage_service import ObjectStorageService
from app.services.task_service import TaskService
from app.services.metadata_service import MetadataService
from app.utils.util import write_to_temp_file

from app.jobs.worker import process_tasks


app = FastAPI()
USER = os.getenv("DB_USER", "root")
PASS = os.getenv("DB_PASS", "root")
HOST = os.getenv("DB_HOST", "localhost")
NAME = os.getenv("DB_NAME","phone_numbers")
DATABASE_URI = f"postgresql://{USER}:{PASS}@{HOST}/{NAME}"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URI)

obj_service = ObjectStorageService(DesktopOS(os.path.join(os.getcwd(), "buckets", "tasks")))
md_service = MetadataService(db)
task_service = TaskService(obj_service, md_service)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/task/{task_id}/results")
def get_results(task_id: str):
    return task_service.get_results(task_id)


@app.get("/tasks")
def get_results():
    return task_service.list()


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    temp = None
    try:
        temp = write_to_temp_file(file)
        response = task_service.create(temp, file.filename)
        return response
    except Exception as e:
        return {"message": "There was an error processing the file " + str(e)}
    finally:
        if temp:
            os.remove(temp.name)


def create_scheduler():
    background_scheduler = BlockingScheduler()
    # background_scheduler.configure()
    background_scheduler.add_job(
        process_tasks,
        kwargs={"db": db, "object_storage_service": obj_service},
        trigger="interval",
        seconds=5,
    )
    return background_scheduler

print("STARTING SCHEDULER")
scheduler = create_scheduler()
from threading import Thread
thread = Thread(target=scheduler.start)
thread.start()

if __name__ == "__main__":
    scheduler = None
    try:
        if os.getenv("ASYNC"):
            print("STARTING SCHEDULER")
            scheduler = create_scheduler()
            scheduler.start()
        else:
            print("STARTING SERVER")
            uvicorn.run(app, host="0.0.0.0", port=8000)

     
    except Exception as e:
        print(e)
        if scheduler:
            scheduler.shutdown()
    finally:
        print("Shutting down")
