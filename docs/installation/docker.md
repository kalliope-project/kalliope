# Run Kalliope in Docker

## Get the image

### From docker hub

Pull the image from [Docker Hub](https://hub.docker.com/r/kalliope/kalliope_ubuntu)

```shell
docker pull kalliope/kalliope_ubuntu:18.04
```

### From a local build

Get the project

```shell
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope/docker/official_image
```

Build the image

```shell
docker build --force-rm=true \
-t kalliope \
-f ubuntu_18_04.dockerfile .
```

## Usage

By default, Kalliope directly uses alsa for audio capture & playback.
The container has the pulseaudio alsa plugin, in order to use the host pulse server without conflicting.
Run the command below to pass your local sound socket to the container.

```shell
docker run -it --rm --name kalliope \
--volume=/run/user/$(id -u)/pulse:/run/user/1000/pulse \
kalliope
```

Then, in the container execute kalliope

```shell
kalliope@397b317c4921:~$ kalliope start
Starting Kalliope
Press Ctrl+C for stopping
Starting order signal
je suis prête
```

Use a volume to mount your brain et settings. E.g:

```shell
docker run -it --rm --name kalliope \
--volume=/run/user/$(id -u)/pulse:/run/user/1000/pulse \
-v /path/to/my_kalliope_config:/home/kalliope/my_kalliope_config
kalliope
```
