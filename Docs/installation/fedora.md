# Kalliope requirements for Fedora

## Fedora packages requirements

You will need that package to be able to install Kalliope on your system

```bash
sudo dnf install gsl-devel gsl python3-devel dialog \
    portaudio-devel libicu-devel mplayer
```

## Install picotts

Then you will need to install pico2wave (picotts).
Fedora dosen't provides any package, so we will install it in our HOME to not impact the system. That will be easier to remove it later.

Note that Fedora should provide `~/.local/bin` in your PATH. 

```bash
cd /tmp
mkdir -p ~/.local/{bin,lib,share}
wget https://raw.githubusercontent.com/stevenmirabito/asterisk-picotts/master/picotts-install.sh
# call install script replacing
# default path
sed 's,\s/usr/, ~/.local/,g' picotts-install.sh | bash

# change pico2wave binary name to create our own
mv ~/.local/bin/pico2wave ~/.local/bin/pico2wave.orig
```

Because we installed pico2wave in "local" dir, we need to force pico2wave to check librairies in another directory. That will be done by adding LD_LIBRARY_PATH env in our own launch script.

Note: we moved pico2wave binary to pico2wave.orig to not have conflict when we will call "pico2wave" without absolute path.

So, create a file `~/.local/bin/_pico2wave`

```bash
#!/bin/bash
export LD_LIBRARY_PATH=~/.local/lib
~/.local/bin/pico2wave.orig "$@"
```

Make it executable: `chmod +x ~/.local/bin/_pico2wave`

Because Kalliope has `/usr/bin/pico2wave` hardcoded in the sourcecode, you need to link this script in `/usr/bin`

```
sudo ln -s ~/.local/bin/_pico2wave /usr/bin/pico2wave
```

Now try this:

```bash
cd /tmp
# Fake pipeline
# Afterward, you can remove out.wav file that is a simple symlink
ln -s /dev/stdout out.wav
# try
pico2wave -l "en-US" -w out.wav "Hello my friend, nice to meet you" | play -
```

You should hear your computer speaking to you.

## Fix libcblas problem

libcblas is not installed as in Ubuntu, so you can link gsl library like that:

```
sudo ln -s /usr/lib64/libgslcblas.so /usr/lib64/libcblas.so
```

# Install Kalliope in a virtualenv

To not impact the entire system, one more time, we will work locally:

```
cd ~
mkdir -p Projects/Kalliope
python -m venv Projects/Kalliope
source ~/Projects/Kalloiope/bin/activate
pip install kalliope
```

Then follow [Quickstart](quickstart.md) page to check if everything is ok.

# Tips

You will need to type `source ~/Projects/Kalloiope/bin/activate` command each time you will want to use Kalliope. If you want a local script to call Kallope without that, please create a script in ~/.local/bin/kalliope:

```
#!/bin/bash
source ~/Projects/Kalloiope/bin/activate
~/Projects/Kalliope/bin/kalliope $@
```

And `chmod +x ~/.local/bin/kalliope`.

# Delete picotts

If you want to remove our picotts installation:

```bash
find ~/.local -name "*tts*" -exec rm -rf "{}" \;
find ~/.local -name "*pico*" -exec rm -rf "{}" \;
sudo rm -rf /usr/bin/pico2wave
```

# Delete Kalliope

Because we installed it on HOME, this is easy.

You'll need this:

```bash
rm -f ~/.local/bin/kalliope
rm ~/Projects/Kalliope
```

And remove libcblas link:

```bash
sudo rm -f /usr/lib64/libcblas.so
```
