FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat -y

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./wait-for-db.sh /app/wait-for-db.sh

ENTRYPOINT [ "/app/wait-for-db.sh" ]
