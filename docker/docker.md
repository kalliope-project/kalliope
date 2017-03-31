# Docker deployment and tests

## Create images

### Ubuntu 16.04
Build the image for Ubuntu 16.04. By default, the master branch of the Kalliope project will be cloned.
```
docker build --force-rm=true -t kalliope-ubuntu1604 -f docker/ubuntu_16_04.dockerfile .
```

To build with TRAVIS env we need to send global variables
```
docker build \
--force-rm=true \
--build-arg TRAVIS_BRANCH=${TRAVIS_BRANCH} \
--build-arg TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE} \
--build-arg TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG} \
--build-arg TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH} \
-t kalliope-ubuntu1604 \
-f docker/ubuntu_16_04.dockerfile .
```

### Debian Jessie
Build the image for Debian Jessie. By default, the master branch of the Kalliope project will be cloned.
```
docker build --force-rm=true -t kalliope-debian8 -f docker/debian8.dockerfile .
```

To build with TRAVIS env we need to send global variables
```
docker build \
--force-rm=true \
--build-arg TRAVIS_BRANCH=${TRAVIS_BRANCH} \
--build-arg TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE} \
--build-arg TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG} \
--build-arg TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH} \
-t kalliope-debian8 \
-f docker/debian8.dockerfile .
```

## Run the test

Ubuntu image
```
docker run -it --rm kalliope-ubuntu1604
```

Debian image
```
docker run -it --rm kalliope-debian8
```
