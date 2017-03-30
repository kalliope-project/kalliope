# Docker deployment and tests

## Create images

Build the image for Ubuntu 16.04.
```
docker build --force-rm=true -t kalliope-app -f ubuntu_16_04.dockerfile .
```

If we want a specific branch of Kalliope
```
docker build --force-rm=true --build-arg branch=dev -t kalliope-app -f ubuntu_16_04.dockerfile .
```

## Run the test

Ubuntu image
```
docker run -it --rm kalliope-app
```