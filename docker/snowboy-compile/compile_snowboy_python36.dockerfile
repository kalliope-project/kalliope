# build last version
# docker build --force-rm=true -t compile_snowboy_python36 -f compile_snowboy_python36.dockerfile .

# build specified version
# docker build --force-rm=true --build-arg SNOWBOY_VERSION=1.1.1 -t compile_snowboy_python36 -f compile_snowboy_python36.dockerfile .

# compile into local /tmp/snowboy
# docker run -it --rm -v /tmp/snowboy:/data compile_snowboy_python36

FROM python:3.6-jessie

ARG SNOWBOY_VERSION="1.3.0"

RUN apt-get update
RUN apt-get install -y git make g++ python3-dev libatlas3-base libblas-dev gfortran vim wget libpcre3-dev libtool libatlas-base-dev

# get the last version of swig
RUN wget https://downloads.sourceforge.net/swig/swig-3.0.12.tar.gz && tar xzf swig-3.0.12.tar.gz
RUN cd swig-3.0.12 && \
    ./configure --prefix=/usr \
    --without-clisp  \
    --without-maximum-compile-warnings && \
    make

RUN cd swig-3.0.12 && \
    make install && \
    install -v -m755 -d /usr/share/doc/swig-3.0.12 && \
    cp -v -R Doc/* /usr/share/doc/swig-3.0.12

RUN wget https://github.com/Kitt-AI/snowboy/archive/v${SNOWBOY_VERSION}.tar.gz && tar xzf v${SNOWBOY_VERSION}.tar.gz

RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python3 && make
RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python3 && python3 -c "import _snowboydetect; print('OK')"
# compiled binary will be placed into data folder
RUN mkdir /data
CMD cp /snowboy-*/swig/Python3/*.so /data
