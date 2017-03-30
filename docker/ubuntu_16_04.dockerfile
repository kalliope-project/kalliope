FROM ubuntu:16.04

ENV no_proxy="127.0.0.1,localhost,kalliope.fr"

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ xenial multiverse" >> /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    sox libatlas3-base mplayer wget \
    && rm -rf /var/lib/apt/lists/*

# Install the last PIP
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

