FROM python:3.8-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add bash build-base gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install -r requirements.txt

