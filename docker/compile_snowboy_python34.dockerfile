# build last version
# docker build --force-rm=true -t compile-snowboy-python34 -f compile_snowboy_python34.dockerfile .

# build specified version
# docker build --force-rm=true --build-arg SNOWBOY_VERSION=1.1.1 -t compile-snowboy-python34 -f compile_snowboy_python34.dockerfile .

# compile into local /tmp/snowboy
# docker run -it --rm --mount type=bind,source=/tmp/snowboy,target=/data compile-snowboy-python34

FROM ubuntu:trusty

RUN apt-get update
RUN apt-get install -y git make g++ python3-dev libatlas3-base libblas-dev gfortran vim wget libpcre3-dev

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

# version can be 1.2.0, 1.1.1, 1.1.0, 1.0.4
ARG SNOWBOY_VERSION="1.2.0"

RUN wget https://github.com/Kitt-AI/snowboy/archive/v${SNOWBOY_VERSION}.tar.gz && tar xzf v${SNOWBOY_VERSION}.tar.gz

RUN sed -i "s|python-config|python3-config|g" snowboy-${SNOWBOY_VERSION}/swig/Python/Makefile
RUN sed -i "s|-lf77blas -lcblas -llapack_atlas -latlas|-lquadmath -lgfortran -lblas /usr/lib/libcblas.so.3|g" snowboy-${SNOWBOY_VERSION}/swig/Python/Makefile
RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python && make
RUN cd /snowboy-${SNOWBOY_VERSION}/swig/Python && python3 -c "import _snowboydetect; print('OK')"
# compiled binary will be placed into data folder
RUN mkdir /data
CMD cp /snowboy-*/swig/Python/*.so /data
