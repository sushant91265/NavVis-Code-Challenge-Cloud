FROM python:3.9.0-alpine
RUN apk add --no-cache bash

ADD . server
WORKDIR server

RUN rm -r env
RUN rm -r temp

RUN mkdir -p buckets/tasks
RUN chmod u+x docker/app/run.sh

RUN python -m venv env
RUN source env/bin/activate
RUN env/bin/pip install -U pip
RUN env/bin/pip install -r req.txt

ENTRYPOINT ["/bin/bash", "-c", "./docker/app/run.sh"]
CMD ["env/bin/python", "api.py"]