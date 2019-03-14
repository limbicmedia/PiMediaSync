# Miniature World Sawmill Exhibit

## Install
### Step 1 - Install Raspbian operating system
Download [Linux Debian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) and unzip the file. This will result in a `.dmg` file

#### MacOS
Place SDCard in card reader. The card will mount, which will prevent the installation step. 

Find where the card is mounted with:

```
diskutil list
```

from the list, find the `disk` associated with the SD card and unmount it with the command:

```
diskutil unmountDisk /dev/disk#
```

Finally, write the Raspbian image to the SD card:
```
sudo dd if=<raspbian image name>.img of=/dev/rdisk# bs=1m
```

### Step 2 - Enable SSH in Raspbian (optional)
After Raspbian is written to the SD card, a drive called `boot` will be mounted. Create a file on this mounted drive called `ssh`.

#### MacOS
Run this command:
```
touch /Volumes/boot/ssh
```

### Step 3 - Unmount SD Card
Once again, run:

```
diskutil unmountDisk /dev/disk#
```

to be able to pull the SD card out. Putting the SD card into the PI and boot.

**Note** All subsequent steps are performed on the Raspberry PI. This can be done by attaching a keyboard and mouse OR by `SSH`ing in (assuming Step 2 was performed)

### Step 4 - Expand Filesystem. , either attach a monitor and keyboard OR
On the Pi, run:
```
sudo raspi-config
```

Select: `7 Advanced Options` 
Followed by: `A1 Expand Filesystem`

Then reboot the system with by running:
```
sudo reboot
```

### Step 5 - Install 
On the Raspberry PI, run:

```
wget -O - https://raw.githubusercontent.com/limbicmedia/mini-world-sawmill-display/master/scripts/install.sh | bash
```

This will install all the necessary requirements (including downloading this git repo)

### Step 6 - Add Video File (Optional; for systems using video)
The desired video should be copied onto the Raspberry PI. The video can have any name and be stored at any location. It may be best to store it in the `mini-world-sawmill-display` directory:

```
/root/mini-world-sawmill-display/video
```

Once the file is copied over, the  `config.py` (located at `/root/mini-world-sawmill-display`) must be modified such that the `VIDEONAME` variable points to the directory and filename of the video. For example, the original value for this variable is:

```
VIDEONAME = "./video/sawmill.mov"
```

In this case, the video is called `sawmill.mov` and it is located--relatively to the starting point of the Python program--in a directory called `video`.

**Note**: When setting `VIDEONAME` it would be best to set the value with an **ABSOLUTE** file path, e.g. `/home/pi/myvideo.mov`.


## System Diagram
Below is an image showing the architecture of the system:
<br>
<img src="docs/system_diagram.png" width="332" height="668">

## Button Wiring
The button for starting the installtion is wired as show below:
<br>
<img src="docs/rpi_button.png" width="100%">
<br>
This wiring results in the code to check for a **FALLING** edge of on GPIO15 (pin 10) to activate the installation. The *1K* resistor acts as a *Pull Up* resistor and the *1µF* capacitor helps reduce noise in the system.