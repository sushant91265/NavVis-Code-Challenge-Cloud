#!/bin/bash
set -e
source env/bin/activate
echo ">>> Which Python"
which Python

echo ">>> runnning db migrations"
echo $DB_HOST
cd db
alembic upgrade head
cd ..

echo "RUN THE PYTHON FILE"
python api.py
