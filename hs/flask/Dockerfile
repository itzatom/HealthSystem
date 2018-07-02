FROM python:latest

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5001

ADD . /usr/src/app

