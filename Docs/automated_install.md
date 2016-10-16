# kalliope automated install

Clone the project
```
cd
git clone https://github.com/kalliope-project/kalliope.git
```

Run the install script.
```
./kalliope/install/install_kalliope.sh
```

>**Note:** The install script must not be ran as root or with sudo. 
You will be prompted to enter your sudo password during the installation process.

To ensure that you can record your voice, run the following command to capture audio input from your microphone
```
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```
play test.wav
```

If everything is ok, you can start playing with Kalliope. First, let's take a look to the [default settings](settings.md).