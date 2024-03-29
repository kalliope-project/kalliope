# BUILD
#docker build \
#--force-rm=true \
#--build-arg TRAVIS_BRANCH=fix-install \
#-t kalliope-ubuntu2004-testing \
#-f docker/testing_ubuntu_20_04.dockerfile .

# RUN
# docker run -it --rm kalliope-ubuntu2004-testing
FROM ubuntu:20.04

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ focal multiverse" >> /etc/apt/sources.list

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris
# install packages
RUN apt-get update && apt-get install -y \
    git python3-dev libsmpeg0 libttspico-utils libsmpeg0 flac \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    libatlas3-base mplayer wget vim sudo locales alsa-base alsa-utils \
    pulseaudio-utils libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

RUN  wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

RUN  pip3 install pyaudio "ansible==4.5.0"

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# add a standart user
RUN useradd -m -u 1000 kalliope
RUN usermod -aG sudo kalliope
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

ADD docker/clone_and_test.sh /home/kalliope/clone_and_test.sh
RUN chown kalliope /home/kalliope/clone_and_test.sh

USER kalliope
WORKDIR /home/kalliope

# run tests
CMD ./clone_and_test.sh