#!/bin/bash
set -e
source env/bin/activate
echo ">>> Which Python"
which python


echo $ASYNC
if [ "$ASYNC" != "1" ]; then
    echo ">>> runnning db migrations"
    echo $DB_HOST
    cd db
    alembic upgrade head
    cd ..
fi

pwd
ls

echo "RUN THE PYTHON FILE"
python api.py


