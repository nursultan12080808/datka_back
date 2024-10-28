FROM python:3.12.7-alpine3.19

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY . /app
EXPOSE 8008

RUN adduser --disabled-password app-user
RUN chown -R app-user:app-user /app
RUN mkdir -p media
RUN chmod -R 777 /app/static/static_root
RUN chmod -R 777 /app/media
RUN chown app-user:app-user -R /app/
RUN pip install -r requirements.txt

USER app-user
