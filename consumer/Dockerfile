FROM python:3.5-slim

WORKDIR /app

COPY kafka_consumer.py /app/.
COPY kafka_repository.py /app/.
COPY requirements.txt /app/.

RUN apt-get update -y \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && apt-get install -y g++ libpq-dev \
    && pip install -r /app/requirements.txt

ENTRYPOINT ["python", "/app/kafka_consumer.py"]
