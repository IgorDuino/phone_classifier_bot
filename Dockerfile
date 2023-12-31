FROM python:3.11-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install -U pip setuptools wheel
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
