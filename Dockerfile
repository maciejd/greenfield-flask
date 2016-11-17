FROM ubuntu:latest
RUN apt-get update
ENV FLASK_APP=greenfield.py

RUN apt-get install -y -q build-essential python-pip python-dev python-simplejson git
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

RUN mkdir deployment
COPY . /deployment/
RUN ls -la /deployment/*
RUN virtualenv /deployment/env/
RUN /deployment/env/bin/pip install Flask
RUN /deployment/env/bin/pip install Flask-SQLAlchemy
WORKDIR /deployment
RUN env/bin/python -c 'from database import init_db; init_db()'
CMD env/bin/flask run --host=0.0.0.0
