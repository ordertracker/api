FROM python:3.7-alpine
MAINTAINER Ilche Bedelovski <ilche.bedelovski@gmail.com>

RUN apk add --no-cache python3-dev && \
    apk add --no-cache gcc && \
    apk add --no-cache g++ && \
    apk add --no-cache libffi-dev && \
    apk add --no-cache git libxml2-dev libxslt-dev musl-dev libgcc openssl-dev curl jpeg-dev zlib-dev 

COPY app/ /srv/app
COPY conf/ /srv/app
COPY wsgi.py /srv/app
COPY requirements.txt /srv/app
WORKDIR /srv/app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV FLASK_APP=wsgi.py
EXPOSE 5000

CMD flask run --host=0.0.0.0
