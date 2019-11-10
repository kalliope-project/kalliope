FROM python:3.6-buster

# Need some packages in non-free repo
RUN sed -i -- 's/buster main/buster main contrib non-free/g' /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python3-dev libpython3-dev libsmpeg0 libttspico-utils libsmpeg0 flac \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    sox libatlas3-base mplayer wget vim sudo locales \
    python3-pip pulseaudio-utils libasound2-plugins python3-pyaudio libasound-dev \
    libportaudio2 libportaudiocpp0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

#RUN  pip3 install pyaudio

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
