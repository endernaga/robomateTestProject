FROM python:3.10.4-slim-buster
LABEL maintainer="endernagashuhsman@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/telegram_bot

RUN python main.py