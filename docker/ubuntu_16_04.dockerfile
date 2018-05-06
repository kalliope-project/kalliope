FROM ubuntu:16.04

ENV no_proxy="127.0.0.1,localhost,kalliope.fr"

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ xenial multiverse" >> /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    sox libatlas3-base mplayer wget vim sudo\
    && rm -rf /var/lib/apt/lists/*

# Install the last PIP
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# fix install in container
RUN pip install --upgrade pip six
RUN pip install --upgrade pip pyyaml
RUN pip install --upgrade pip SpeechRecognition
RUN pip install --upgrade pip Werkzeug
RUN pip install --upgrade pip gitdb

# add a standart user. tests must not be ran as root
RUN useradd -m -u 1000 tester
RUN usermod -aG sudo tester
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# get TRAVIS environment variables
ARG TRAVIS_BRANCH
ARG TRAVIS_EVENT_TYPE
ARG TRAVIS_PULL_REQUEST_SLUG
ARG TRAVIS_PULL_REQUEST_BRANCH
ENV TRAVIS_BRANCH=${TRAVIS_BRANCH}
ENV TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE}
ENV TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG}
ENV TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH}

ADD docker/clone_and_test.sh /home/tester/clone_and_test.sh
RUN chown tester /home/tester/clone_and_test.sh

USER tester
WORKDIR /home/tester

# run tests
CMD ./clone_and_test.sh