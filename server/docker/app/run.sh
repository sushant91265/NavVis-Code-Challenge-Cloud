#!/bin/bash
set -e
source env/bin/activate
echo ">>> Which Python"
which python

# TODO: why needed?
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


