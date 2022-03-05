# build last version
# docker build --force-rm=true -t compile_snowboy_python39 -f compile_snowboy_python39.dockerfile .

# build specified version
# docker build --force-rm=true --build-arg SNOWBOY_VERSION=1.1.1 -t compile_snowboy_python39 -f compile_snowboy_python39.dockerfile .

# compile into local /tmp/snowboy
# docker run -it --rm -v /tmp/snowboy:/data compile_snowboy_python39

FROM python:3.9-bullseye

ARG SNOWBOY_VERSION="1.3.0"

RUN apt-get update
RUN apt-get install -y git make g++ python3-dev libatlas3-base libblas-dev \
    gfortran vim wget libpcre3-dev libtool libatlas-base-dev swig

RUN wget https://github.com/Kitt-AI/snowboy/archive/v${SNOWBOY_VERSION}.tar.gz && tar xzf v${SNOWBOY_VERSION}.tar.gz

RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python3 && make
RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python3 && python3 -c "import _snowboydetect; print('OK')"
# compiled binary will be placed into data folder
RUN mkdir /data
CMD cp /snowboy-*/swig/Python3/*.so /data
