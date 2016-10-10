# kalliope automated install

Clone the project
```
cd
git clone https://repo/kalliope.git
```

Run the install script.
```
./kalliope/install/install_kalliope.sh
```

>**Note:** The install script must not be ran as root or with sudo. 
You will be prompted to enter your sudo password during the installation process.

Be sure you can record you voice, run the following command to capture audio from your microphone
```
rec test.wav
```

Press CTRL-C after capturing a sample of our voice.

Then play the recorded audio file
```
play test.wav
```

If everything is ok, you can start playing with Kalliope. First, 