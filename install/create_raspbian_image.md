# Create a Raspbian image with already installed Kalliope

This documentation aims at explaining how to creta a Raspbian image with pre installed Kalliope.

Install a fresh [image of Raspbian](http://downloads.raspberrypi.org/raspbian/images/) as usual on your raspberry Pi.
Once deployed, follow manual steps bellow.

>**Note:** From here I suppose that the Rpi has received a valid IP from your LAN DHCP server and can access to the internet.

## Prepare the image
Login to your Rpi.

Enable SSH
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

You now have a SSH connection, you can connect remotely to your Pi to perform next steps from a console.

>**Note:** The SSH server is listening on the default SSH port with the default Rasbpian credentials. This can be a security issue.
It is recommended  to check that the Rpi is not directly accessible from the internet.

Install Kalliope from the script
```bash
curl -s https://raw.githubusercontent.com/kalliope-project/kalliope/master/install/rpi_install_kalliope.sh | bash
```

If you want to install a particular branch you can specify it with an argument following the syntax bellow
```
curl -s https://raw.githubusercontent.com/kalliope-project/kalliope/master/install/rpi_install_kalliope.sh | bash -s <branch_name>
```

E.g
```bash
curl -s https://raw.githubusercontent.com/kalliope-project/kalliope/master/install/rpi_install_kalliope.sh | bash -s dev
```

Check Kalliope is installed
```bash
kalliope --version
```
Configure locales
```
locale-gen en_US.UTF-8
```

```
sudo dpkg-reconfigure locales
```

Edit `~/.bashrc` and add those line at the end of the file
```
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"
```

Try to run the default config
```
kalliope start
```

Cleanup installation files
```bash
rm -rf get-pip.py
sudo rm -rf kalliope
```

Clone some starter kit
```bash
git clone https://github.com/kalliope-project/kalliope_starter_fr.git
git clone https://github.com/kalliope-project/kalliope_starter_en.git
git clone https://github.com/kalliope-project/kalliope_starter_de.git
```

Change the hostname
```bash
sudo hostnamectl set-hostname kalliope
sudo sed -i 's/raspberrypi/kalliope/g' /etc/hosts
```

Clear the command line history
```bash
cat /dev/null > /home/pi/.bash_history && history -c
```

Shutdown the Rpi
```bash
sudo shutdown -h now
```

## Create the image

Next commands have been tested on Ubuntu 16.04.

In the next part we create an image an shrink it in order to take less storage space.
>**Note:** Raspbian operating system comes with a tool to resize the filesystem to the largest size the SD card will support (sudo raspi-config, then select Expend Filesystem). You wont lose space by shrinking the image because you can expand it back again.

>**Note:** Be sure of what you doing in next steps. Writing disk image on the wrong disk will destroy all your computer data. 

Remove the SD card from your Rpi and connect it into a Linux distrib via an external USB card reader.

Check where the card is mounted
```bash
df -h
```

The output should looks like this
```bash
df -h
Filesystem      Size  Used Avail Use% Mounted on
--- TRUNCKATED ---
/dev/sdb2        15G  1.3G   13G  10% /media/nico/f2100b2f-ed84-4647-b5ae-089280112716
/dev/sdb1        41M   21M   21M  51% /media/nico/boot
```

The SD card is on **/dev/sdb device**. It has two partition, **/dev/sdb1** and **/dev/sdb2**.

>**Note:** Your system might mount the card somewhere else depending on the number of disk you already have like /dev/sdc or /dev/sde. 
Note down the path where your SD is.

Unmount the two partitions. Keep the SD card in the reader and connected to the system.
```bash
sudo umount /dev/sdb1 /dev/sdb2
```

Make the image with **dcfldd**. This program is a replacement for the old dd disk utility program that show the progression of a copy.

Install the tool
```bash
sudo apt-get install dcfldd
```

Create the image following this syntax.
```
sudo dcfldd if=<my_sd_card_disk_path> of=<target_path>/kalliope.img
```

E.g
```bash
sudo dcfldd if=/dev/sdb of=kalliope.img
```
>**Note:** Be sure you have enough space available in the target path

It will take a couple minutes to create the image depending of the size of your SD card.

Once it's done, give the ownership back to your current user. (the image belong to root as we created it with sudo)
```bash
sudo chown ${USER}:${USER} kalliope.img
```

Now we have a file that can already be used to instantiate a Rpi. But the file is big as the SD card itself.
To reduce the size of the image we need `gparted`. Install it
```bash
sudo apt-get install gparted
```

Gparted is only able to edit physical device, so we need to create a virtual device from the image before using it.
As we saw when we have identified our disk, Raspbian has two partitions. The fist one, boot, is already tiny and does not need to be shrank.
The second partition is where everything is stored. It contains a lot of free space.

Show partition info from the image
```bash
sudo fdisk -l kalliope.img
```

The output should looks like this
```
Device        Boot Start      End  Sectors  Size Id Type
kalliope.img1       8192    92159    83968   41M  c W95 FAT32 (LBA)
kalliope.img2      92160 31116287 31024128 14.8G 83 Linux
```

Export the START sector of the second partition. The variable will be used in next commands.
```bash
export START=92160
```

Check the env variable is set correctly
```bash
echo ${START}
```

Create the virtual drive with only the second patition
```bash
sudo losetup /dev/loop0 kalliope.img -o $((START*512))
```

Now read the loopback device with gparted
```bash
sudo gparted /dev/loop0
```

Gparted will show you the state of the partition. Click the `/dev/loop0` partition and select **Resize/Move** from the menu.
change the value of "New Size" so that it is slighty abose the "Minimum Size". 
Note down the new size! In this example the new size is **2000 MB**.
Then apply the resizing and exit gparted.

Remove the loopback device and create a new one with the whole image this time.
```bash
sudo losetup -d /dev/loop0
sudo losetup /dev/loop0 kalliope.img
```

Now, we use **fdisk** to edit the partition table in order to resize it to the new size.
```bash
sudo fdisk /dev/loop0
```

You should now see the **fdisk** prompt.
- Enter **d 2** to delete the table entry for the second partition
- Enter n p 2 to create a new second partition entry
- Enter the START sector number that you used earlier.
- Enter `+NEWSIZE` as the new size. Don't forget the "+" at the start. For example `+2000M`
- Enter w to write the new partition


Output example
```
Command (m for help): d
Partition number (1,2, default 2): 2

Partition 2 has been deleted.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (2048-31116287, default 2048): 92160
Last sector, +sectors or +size{K,M,G,T,P} (92160-31116287, default 31116287): +2000M

Created a new partition 2 of type 'Linux' and of size 2 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
```
Let's take a look to the partition table again
```
sudo fdisk -l /dev/loop0

Device       Boot Start     End Sectors Size Id Type
/dev/loop0p1       8192   92159   83968  41M  c W95 FAT32 (LBA)
/dev/loop0p2      92160 4188159 4096000   2G 83 Linux
```

Note down the ED sector of the second partition
```bash
export END=4188159
```

Destroy the loopback
```bash
sudo losetup -d /dev/loop0
```

Now, trim the file to the new length.
```
truncate -s $(((END+1)*512)) kalliope.img
```

Check the new size of the image
```bash
du -hs kalliope.img 
2.0G	kalliope.img
```

You can now compress it to reduce a little more the size
```bash
zip kalliope.img.zip kalliope.img
```

Final size
```bash
du -hs kalliope.img.zip 
727M	kalliope.img.zip
```
