FROM python:3.9.0-alpine
RUN apk add --no-cache bash

ADD . server
WORKDIR server

RUN mkdir -p downloads
RUN chmod u+x docker/app/run.sh

RUN python -m venv env
RUN source env/bin/activate
RUN env/bin/pip install -U pip
RUN env/bin/pip install -r req.txt

ENTRYPOINT ["/bin/bash", "-c", "./docker/app/run.sh"]