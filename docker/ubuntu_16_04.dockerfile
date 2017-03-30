FROM ubuntu:16.04

ENV no_proxy="127.0.0.1,localhost,kalliope.fr"

# pico2wav is a multiverse package
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ xenial multiverse" >> /etc/apt/sources.list

# install packages
RUN apt-get update && apt-get install -y \
    git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog \
    libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    sox libatlas3-base mplayer wget vim\
    && rm -rf /var/lib/apt/lists/*

# Install the last PIP
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# add a standart user. tests must not be ran as root
RUN useradd -m -u 1000 tester

# by default we get the master branch. We can override this by adding
ARG branch=master
RUN cd /home/tester && git clone https://github.com/kalliope-project/kalliope.git
RUN cd /home/tester/kalliope && git checkout ${branch} && python setup.py install
RUN chown -R tester:tester /home/tester/kalliope

USER tester
WORKDIR /home/tester/kalliope

# run tests
CMD ["python", "-m", "unittest", "discover"]
