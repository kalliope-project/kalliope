# Docker deployment and tests

## Create images

Build the image for Ubuntu 16.04
```
docker build --force-rm=true -t kalliope-app -f ubuntu_16_04.dockerfile .
```