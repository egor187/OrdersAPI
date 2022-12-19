FROM python:3.11-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY /requirements /requirements

RUN pip3 install -r /requirements/base.txt

COPY . .
