# used to build the last kalliope dev version with python 3
# docker build --force-rm=true -t kalliope-ubuntu1604-python3 -f docker/ubuntu_16_04_python3.dockerfile .
# docker run -it --rm kalliope-ubuntu1604-python3

FROM ubuntu:16.04

ENV no_proxy="127.0.0.1,localhost,kalliope.fr"

# set UTF-8 to the terminal
ENV LANG en_US.UTF-8

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ xenial multiverse" >> /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python3-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    sox libatlas3-base mplayer wget vim sudo\
    && rm -rf /var/lib/apt/lists/*

# Install the last PIP
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# add a standart user. tests must not be ran as root
RUN useradd -m -u 1000 tester
RUN usermod -aG sudo tester
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

ADD docker/clone_and_test_python3.sh /home/tester/clone_and_test_python3.sh
RUN chown tester /home/tester/clone_and_test_python3.sh

USER tester
WORKDIR /home/tester

# run tests
CMD ./clone_and_test_python3.sh