FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y mc

COPY monitor.py .
RUN pip install minio pandas scikit-learn elasticsearch