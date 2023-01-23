## The Assignment
- Please see README_Cloud.html for the details.


## Tech Stack
- Python 3.9.0
- FastAPI
- PostgreSQL 11
- Minio(object storage)
- Nginx
- Docker
- Alembic(for DB migration)
- Unittest
- Coverage


## Classes
- TaskService: Deals with Task related operations.
- MetadataService: Abstraction layer for the database.
- ObjectStorageService: Deals with minion related operations.
- api: Contains the api endpoints.
- worker: Fetches tasks from the database and processes them.
- app/dto/models: Pojo classes.
- db/model: Database models.


## How to run the application
- Run `docker-compose up --build` in the server directory of the project.
- The application api's will be available at http://localhost:8000/docs


## Assumptions
- The application is running on a Linux machine.
- The file size is less than the available memory.
- Deleteing results meaning deleting the phone numbers from the database not the taskId.
- If the user queries before the whole file is processed, we return partial results.
- Currently passwords are hardcoded in the docker-compose.yml file. In production, we should use secrets.
- Even if there is space in phone number, we consider it as a valid phone number.


## Project Structure
- The project is divided into 4 parts.
- The `app` directory contains the application code.
- The `db` directory contains the database code.
- The `tests` directory contains the tests.
- The `docker` directory contains the docker files.


## Database Schema and DFD
- Please see the <table_name>_schema.png and Upload_Flow.png files in the resources directory of the project.


## Testing
- Make sure to run `pip install -r req.txt` in the server directory of the project.
- The application is tested using unittest.
- The tests are located in the tests directory of the project.
- Run individual file unit tests using `python3 -m unittest tests/jobs/test_worker.py` or run all unit tests using `python3 -m unittest discover tests`, inside the server directory of the project.
- Run integration tests using `sh integration_test.sh` inside the root directory of the project.(make sure you have `jq` intsalled on your machine.)
- Coverage report can be generated using `coverage run -m unittest discover tests`, `coverage report` and `coverage html` inside the server directory of the project.


## Troubleshooting
- Using `docker exec -it <container_id> bash` you can get into the container and see the logs in the /var/log/nginx/error.log file and the application logs in the /app/app.log file.
- Also, you can use `docker logs <container_id>` to see the logs.
- Similarly enter into the database container and use `psql phone_numbers` to get into the database and use `select * from <table_name>;` to see the data in the database.
- `\d <table_name>` to see the schema of the table.
- If you try to run the application without using docker-compose, then alembic generation(under `db` directory) will be needed. Please refer to the alembic official documentation for more details. [https://alembic.sqlalchemy.org/en/latest/]
- Delete `/var` directory in the root directory of the project if you want to start from scratch.