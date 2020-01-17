FROM python:3.7-alpine
#FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

COPY ./requirements.txt /requirements.txt

RUN apk update \
    && \
    apk upgrade \
    && \
    apk add \
      bash \
      vim \
      build-base \
    && \
    pip install --upgrade pip \
    && \
    pip install -r /requirements.txt

WORKDIR /app
CMD /usr/local/bin/python sockets.py
#CMD gunicorn -k gevent -w 1 --bind 0.0.0.0:8000 main:app
#CMD gunicorn -k eventlet -w 1 --bind 0.0.0.0:8000 main:app
