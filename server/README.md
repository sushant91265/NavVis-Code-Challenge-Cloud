## The Assignment
- Please see README_Cloud.html for the details.


## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Minio
- Nginx
- Docker
- Alembic


## How to run the application
- Run `docker-compose up --build` in the server directory of the project.
- The application api's will be available at http://localhost:8000/docs


## Assumptions
- The application is running on a Linux machine.
- The file size is less than the available memory.
- Deleteing results meaning deleting the phone numbers from the database not the taskId.
- If the user queries before the whole file is processed, we return partial results.
- Currently passwords are hardcoded in the docker-compose.yml file. In production, we should use secrets.


## Project Structure
- The project is divided into 4 parts.
- The `app` directory contains the application code.
- The `db` directory contains the database code.
- The `tests` directory contains the tests.
- The `docker` directory contains the docker files.


## Database Schema and DFD
- Please see the <table_name>_schema.png and Upload_Flow.png files in the resources directory of the project.


## Debugging and Testing
- The application is tested using pytest.
- The tests are located in the tests directory of the project.
- The tests can be run using `pytest --cov=app --cov-report=html` command in the server directory of the project to get the coverage report in html format.
- Using `docker exec -it <container_id> bash` you can get into the container and see the logs in the /var/log/nginx/error.log file and the application logs in the /app/app.log file.
- Also, you can use `docker logs <container_id>` to see the logs.
- Similarly enter into the database container and use `psql phone_numbers` to get into the database and use `select * from <table_name>;` to see the data in the database.
- `\d <table_name>` to see the schema of the table.
- If you try to run the application without using docker-compose, then alembic generation(under `db` directory) will be needed. Please refer to the alembic official documentation for more details. [https://alembic.sqlalchemy.org/en/latest/]