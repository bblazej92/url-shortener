FROM ubuntu:16.04

# Upgrade packages
RUN apt-get update -qy --fix-missing
RUN apt-get upgrade -qy
RUN apt-get install -yq python3.5 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python


# Install python requirements
RUN python3.5 -m pip install -U pip
RUN python3.5 -m pip install click==6.7
RUN python3.5 -m pip install Flask==0.12
RUN python3.5 -m pip install flask-mongoengine==0.9.2
RUN python3.5 -m pip install marshmallow==2.13.0
RUN python3.5 -m pip install ujson==1.35
RUN python3.5 -m pip install rauth==0.7.3
RUN python3.5 -m pip install Flask-Login==0.4.0
RUN python3.5 -m pip install freezegun==0.3.8
RUN python3.5 -m pip install Flask-Login==0.4.0
RUN python3.5 -m pip install pip-utils==0.0.6
RUN python3.5 -m pip install rauth==0.7.3
RUN python3.5 -m pip install Flask-Bootstrap==3.3.7.1

RUN apt-get -yq install git
RUN apt-get -yq install vim

# Clone repository
WORKDIR /opt
RUN echo !HASH!
RUN git clone https://github.com/bblazej92/url-shortener.git
WORKDIR url-shortener
RUN git checkout origin/master
