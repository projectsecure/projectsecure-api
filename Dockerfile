FROM python:3.6-onbuild
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /setup/
o

VOLUME /code
WORKDIR /code
COPY . /code
