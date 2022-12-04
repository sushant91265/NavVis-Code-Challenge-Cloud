import uvicorn
import os
import time
from pytz import utc

from fastapi import FastAPI, UploadFile, File
from fastapi_sqlalchemy import DBSessionMiddleware, db
from apscheduler.schedulers.background import BackgroundScheduler

from app.clients.object_storage.desktop import DesktopOS
from app.services.object_storage_service import ObjectStorageService
from app.services.task_service import TaskService
from app.services.metadata_service import MetadataService
from app.utils.util import write_to_temp_file

from app.jobs.worker import process_tasks

app = FastAPI()
DATABASE_URI = 'postgresql://root:root@localhost/phone_numbers'
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URI)

obj_service = ObjectStorageService(DesktopOS(os.getcwd()))
md_service = MetadataService(db)
task_service = TaskService(obj_service, md_service)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/task/{task_id}/results")
def get_results(task_id: str):
    return task_service.get_results(task_id)


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
    background_scheduler = BackgroundScheduler(demon=True)
    background_scheduler.configure(timezone=utc)
    background_scheduler.add_job(process_tasks, kwargs={"db": db, "os": obj_service}, trigger='interval', seconds=5)
    return background_scheduler


if __name__ == "__main__":
    if not os.getenv("ASYNC"):
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        scheduler = create_scheduler()
        scheduler.start()
        uvicorn.run(app, host="0.0.0.0", port=8000)
        scheduler.shutdown()

