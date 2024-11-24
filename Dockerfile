FROM python:3.11
LABEL authors="OldestSalt"

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && pip3 install -r requirements.txt
RUN apt-get install -y python3-opencv

COPY main/ .