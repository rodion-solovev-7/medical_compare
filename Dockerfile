FROM python:3.10.9-slim-bullseye

ARG Test

RUN mkdir -m 777 -p /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN cp config/example.py config/local.py

# TODO: add tini to entrypoints
