# syntax=docker/dockerfile:1
FROM python:3.9.6
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/django/start /start
# RUN sed -i 's/\r//' /start
# RUN chmod +x /start

WORKDIR /code

COPY . /code/



