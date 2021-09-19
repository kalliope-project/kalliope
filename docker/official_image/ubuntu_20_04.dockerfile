# BUILD
#docker build --force-rm=true \
#-t kalliope \
#-f docker/official_image/ubuntu_20_04.dockerfile .

# RUN
# docker run -it --rm \
# --volume=/run/user/$(id -u)/pulse:/run/user/1000/pulse \
# kalliope

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
    python3-pip pulseaudio-utils libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

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

# sound config
COPY docker/official_image/pulse-client.conf /etc/pulse/client.conf
COPY docker/official_image/asound-pulse.conf /etc/asound-pulse.conf
COPY docker/official_image/alsa-pulse.conf   /etc/alsa-pulse.conf
ENV ALSA_CONFIG_PATH=/etc/alsa-pulse.conf
ENV PULSER_SERVER=unix:/run/user/1000/pulse/native

RUN  pip3 install pyaudio "ansible==4.5.0"

# add a standart user
RUN useradd -m -u 1000 kalliope
RUN usermod -aG sudo kalliope
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
WORKDIR /home/kalliope
USER kalliope

# install kalliope from last stable version
# RUN git clone https://github.com/kalliope-project/kalliope.git kalliope && cd kalliope && sudo python3 setup.py install
# Copy local path
COPY . /home/kalliope
# RUN sudo pip3 install --upgrade --force-reinstall setuptools
RUN sudo python3 setup.py install

# fix a lib
# RUN sudo chmod a+r /usr/local/lib/python3.6/dist-packages/httpretty-0.9.6-py3.6.egg/EGG-INFO/requires.txt

