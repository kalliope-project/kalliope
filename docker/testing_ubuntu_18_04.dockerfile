FROM ubuntu:18.04

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ bionic  multiverse" >> /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python3-dev libsmpeg0 libttspico-utils libsmpeg0 flac \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    libatlas3-base mplayer wget vim sudo locales alsa-base alsa-utils \
    python3-distutils pulseaudio-utils libasound2-plugins python3-pyaudio libasound-dev \
    libportaudio2 libportaudiocpp0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN  wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

RUN  pip3 install pyaudio "ansible==2.9.5"

# set UTF-8
ARG lang=en_US
RUN cat /etc/locale.gen | grep ${lang} && \
 sh -c "lang=${lang}; sed -i -e '/${lang}/s/^#*\s*//g' /etc/locale.gen" && \
 cat /etc/locale.gen | grep ${lang} && \
 echo 'LANG="${lang}.UTF-8"'>/etc/default/locale && \
 dpkg-reconfigure --frontend=noninteractive locales && \
 update-locale LANG=${lang}.UTF-8
ENV LC_ALL ${lang}.UTF-8
ENV LC_CTYPE ${lang}.UTF-8

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