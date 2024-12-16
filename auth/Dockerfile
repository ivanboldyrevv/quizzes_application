FROM python:3.13-slim AS base
WORKDIR fastapi_app/

COPY ./ ./

RUN apt-get update && \
    apt-get install -y libpq-dev

RUN pip install fastapi[standard]
RUN pip install peewee
RUN pip install psycopg2-binary
RUN pip install pyjwt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
