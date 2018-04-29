# build last version
# docker build --force-rm=true -t compile_snowboy_python27 -f compile_snowboy_python27.dockerfile .

# build specified version
# docker build --force-rm=true --build-arg SNOWBOY_VERSION=1.1.1 -t compile_snowboy_python27 -f compile_snowboy_python27.dockerfile .

# compile into local /tmp/snowboy
# docker run -it --rm -v /tmp/snowboy:/data compile_snowboy_python27

FROM python:2.7-jessie

ARG SNOWBOY_VERSION="1.3.0"

RUN apt-get update
RUN apt-get install -y git make g++ python-dev libatlas-base-dev gfortran vim wget

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


RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python && make
RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python && python -c "import _snowboydetect; print('OK')"
# compiled binary will be placed into data folder
RUN mkdir /data
CMD cp /snowboy-*/swig/Python/*.so /data
