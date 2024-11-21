FROM python:3.11
LABEL authors="OldestSalt"

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "train.py"]