## Test your env

### Check your microphone and speaker configuration

To ensure that you can record your voice, run the following command to capture audio input from your microphone:

```bash
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file

```bash
mplayer test.wav
```

Your installation is now complete, let's take a look now to the [getting started documentation](../getting-started.md) to learn how to use Kalliope.

### (Optional) Start Kalliope automatically after a reboot

If you want to start Kalliope automatically:

Place the script bellow in `/etc/systemd/system/kalliope.service`.

Update the path `<my_config_path>` with the path where you've placed your `brain.yml` and `settings.yml`.

Update the `<username>` with a non root user. For example, on Raspbian you can set `pi`.

```bash
[Unit]
Description=Kalliope
After=pulseaudio.service

[Service]
WorkingDirectory=<my_config_path>

Environment='STDOUT=/var/log/kalliope.log'
Environment='STDERR=/var/log/kalliope.err.log'
ExecStart=/bin/bash -c "/usr/local/bin/kalliope start > ${STDOUT} 2> ${STDERR}"
User=<username>

[Install]
WantedBy=multi-user.target
```

E.g

```bash
[Unit]
Description=Kalliope
After=pulseaudio.service

[Service]
WorkingDirectory=/home/pi/my_kalliope_config

Environment='STDOUT=/var/log/kalliope.log'
Environment='STDERR=/var/log/kalliope.err.log'
ExecStart=/bin/bash -c "/usr/local/bin/kalliope start > ${STDOUT} 2> ${STDERR}"
User=pi

[Install]
WantedBy=multi-user.target
```

Create both log files and give rights to your user

```bash
sudo touch /var/log/kalliope.log
sudo touch /var/log/kalliope.err.log
sudo chown pi:pi /var/log/kalliope*
```

Then, reload systemctl, start the service and enable it at startup

```bash
sudo systemctl daemon-reload
sudo systemctl start kalliope
sudo systemctl enable kalliope
```

Check that the service is ok

```
sudo systemctl status kalliope
```
