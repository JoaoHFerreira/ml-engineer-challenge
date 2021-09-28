FROM python:3.8-slim


WORKDIR /app

COPY main.py /app/.
COPY api_repository.py /app/.
COPY api_documentation.py /app/.
COPY requirements.txt /app/.

RUN apt-get update -y \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && apt-get install -y g++ libpq-dev \
    && pip install -r /app/requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]