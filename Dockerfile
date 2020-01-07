FROM python:3.7-alpine
#FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

#ENV STATIC_URL /static
#ENV STATIC_PATH /var/www/app/static

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
CMD /usr/local/bin/python main.py

