# Docker 

## Unit Tests

### Create images

#### Ubuntu 20.04

Build the image for Ubuntu 20.04. By default, the master branch of the Kalliope project will be cloned.
```
docker build --force-rm=true -t kalliope-ubuntu1604 -f docker/ubuntu_16_04.dockerfile .
docker build \
--force-rm=true \
-t kalliope-ubuntu2004 \
-f docker/testing_ubuntu_20_04.dockerfile .
```

To build with TRAVIS env we need to send global variables
```
docker build \
--force-rm=true \
--build-arg TRAVIS_BRANCH=${TRAVIS_BRANCH} \
--build-arg TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE} \
--build-arg TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG} \
--build-arg TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH} \
-t kalliope-ubuntu2004 \
-f docker/testing_ubuntu_20_04.dockerfile .
```

#### Debian Buster

Build the image for Debian Jessie. By default, the master branch of the Kalliope project will be cloned.
```
docker build --force-rm=true -t kalliope-debian10 -f docker/testing_debian10.dockerfile .
```

To build with TRAVIS env we need to send global variables
```
docker build \
--force-rm=true \
--build-arg TRAVIS_BRANCH=${TRAVIS_BRANCH} \
--build-arg TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE} \
--build-arg TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG} \
--build-arg TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH} \
-t kalliope-debian10 \
-f docker/testing_debian10.dockerfile .
```

### Run the test

Ubuntu image
```
docker run -it --rm kalliope-ubuntu2004
```

Debian image
```
docker run -it --rm kalliope-debian10
```

## Compile Snowboy

All Snowboy binaries for x86_64 architecture can be compiled from the docker compose file
```bash
mkdir /tmp/snowboy
docker-compose -f compose_compile_snowboy_all.yml up
```

## Compile Snowboy for a Raspberry from amd64 system

Check current platform
```
docker buildx ls
NAME/NODE DRIVER/ENDPOINT STATUS  PLATFORMS
default * docker                  
  default default         running linux/amd64, linux/386
```

Activate arm platforms
```
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

Check
```
docker buildx ls
NAME/NODE DRIVER/ENDPOINT STATUS  PLATFORMS
default * docker                  
  default default         running linux/amd64, linux/386
```

Create a builder
```
docker buildx create --name rpibuilder --driver docker-container --use
```

Bootstrap the builder
```
docker buildx inspect --bootstrap
```

Build the image
```
docker buildx build --platform linux/arm/v7 --load --force-rm=true -t compile_snowboy_python39_rpi -f compile_snowboy_python39.dockerfile .
```

Get the built Snowboy binary
```
docker run -it --rm -v /tmp/snowboy:/data compile_snowboy_python39_rpi
```

