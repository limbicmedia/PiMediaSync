# PiMediaSync

## About
`PiMediaSync` is a small Python application designed for running synchronized audio/video and lighting on a Raspberry PI with the option for user activation (i.e. buttons).

This application was originally designed for use at [Miniature World](https://miniatureworld.com/) for a variety of permanent displays. It has since been broken out into a more general purpose tool and should should be capable of handling any museum or gallery installation requiring ongoing displays of audio/video and/or DMX lighting.

The application has support for user interface (button activation), scheduled activation, and automatic sequencing (media and lighting sequence looping).

The application is designed to run at boot (using a `systemd` service) with all application functionality configured with a config file (see `config.py` for example config setup).

## Features
This application currently supports:

### Media File
Currently, only one media file (video or audio) is supported.

The media file can be nearly any audio or video format (see [OmxPlayer](https://elinux.org/Omxplayer) for details). 

The media file can currently only be played from the **beginning**. However, media files can be stopped before the end of the file through the `LIGHTING_SEQUENCE` (see [example_config.py](./example_config.py)) by setting the last sequence element to stop before the duration of the media file. This is useful in an instance where editing the video file would be cumbersome and ending early is ideal. 

#### Configuration
The configuration variables related to Media Files are outlined below. See [example_config.py](./example_config.py) for a complete example.

The `MEDIA_NAME` variable defines the location of the Media File which will be played. Setting the variable to `None` (or pointing to a non-existent file) will allow the sequence to run without media.

### DMX
DMX lighting is supported through an Enttec USB-to-DMX device. Currently only one DMX device is supported at a time.

#### Configuration
The configuration variables related to DMX are outlined below. See [example_config.py](./example_config.py) for a complete example.

The `DMX_DEVICE` variable defining the file location of the DMX interface (e.g. `/dev/ttyUSB0`). If the application cannot connect to the interface (e.g. missing or wrong filename), an error will be logged but the application will move ahead as if it had an interface.

The `DEFAULT_VALUE` variable defines the starting and ending (before and after the sequence) DMX value for all DMX outputs.

The `DEFAULT_TRANSITION_TIME` variable defines the transition time for the `DEFAULT_VALUE` transition. 

The `CHANNELS` variable is a list which defines the order of DMX channels. This allows for arbitrary mappings of DMX channels.

The `LIGHTING_SEQUENCE` variable defines a sequence of DMX attributes to be moved through in order. Each element in the sequence runs one after another until the end of the sequence. Each sequence element contains:

* `dmx_levels`: a list of DMX brightness levels (0 - 255). The order of the list is mapped to each DMX channel with the `CHANNELS` variable.
* `dmx_transition`: the time (in seconds) for the DMX lights to move from previous state to current brightness levels.
* `end_time`: the time elapsed (in seconds) that the current sequence ends. If the last sequence's `end_time` is less than the video duration, the video ends.


### User Input
Currently, only a single button is supported (more specifically, a single logic high/low on a GPIO pin). When configured, the input will act as a trigger for activating the media/lighting sequence.

The input can only be activated once per sequence and will ignore all presses until the sequence has ended. The input is triggered on the **FALLING** edge of the signal.

If the input is not configured, the application will still run. 

#### Configuration
The `GPIO_VALUES` variable configures the input component. The sub-components of this variables are:

* 'pin': the GPIO pin on the Raspberry PI where the system is configured (e.g. `10` for pin 10 on the PI)
* 'pull_up_down': the state of the *pull up*/*pull down* internal resistor of the system (e.g. `GPIO.PUD_OFF` disables the internal resistor). See the Raspberry PI GPIO [documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/) for more details.

### Timed Trigger
When configured, the input will act as a trigger for activating the media/lighting sequence on a timer. This operates just like the User Input configuration. This trigger is not mutually exclusive with the User Input configuration, however, when a sequence is running it must complete before the activation (button or timer) can trigger it again.

#### Configuration
The `SCHEDULER_TIME` variable sets the timer schedule (in seconds). If the value is `<=` 0, the scheduler is not activated.

### Autorepeat
Instead of running from an activation trigger, the application can be configured to run automatically in a loop. When configured, the application will not accept button or timed triggers and will run automatically from the start, repeating immediately following the end of the sequence.

#### Configuration
The `AUTOREPEAT` variable enables/disables the autorepeat function (`true`/`false`).

## Application Installation
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
**Note**: If SSH is not enabled, a keyboard and mouse will be required for the next steps.

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

to be able to pull the SD card out. Place the SD card into the PI and plug in power.

**Note** All subsequent steps are performed on the Raspberry PI. This can be done by attaching a keyboard and mouse OR by `SSH`ing in (assuming Step 2 was performed)

### Step 4 - Expand Filesystem
On the Pi, run:
```
sudo raspi-config
```

In the blue screen:

Select: `7 - Advanced Options` 
Followed by: `A1 - Expand Filesystem`

Then reboot the system with by running:
```
sudo reboot
```

### Step 5 - Installation
On the Raspberry PI, run:

```
sudo su
export PIMEDIASYNC_VERSION=v1.0.0 # set the branch of PiMediaSync here
wget -O - https://raw.githubusercontent.com/limbicmedia/mini-world-sawmill-display/master/scripts/install.sh | bash
```

This will install all the necessary requirements (including downloading this git repo)

### Step 6 - Add Media File (Optional; for systems using audio/video)
The desired video should be copied onto the Raspberry PI. The video can have any name and be stored at any location.

Once the media file is copied over, modify the configuration file (be default, `/opt/pimediasync/example_config.py`) such that the `MEDIA_NAME` variable points to the directory and filename of the video. For example, if a file called `myvideo.mov` was stored in `/home/pi`, then the variable must be set to:

```
MEDIA_NAME = "/home/pi/myvideo.py"
```

**Note**: A media file is not required since DMX sequencing will work without one.

### Step 6 - Reboot the System
Once all the above steps are run, run:

```bash
reboot
```

## Running the Application
### At Boot
When installed using the [install.sh](./scripts/install.sh) script, the application will be automatically setup to run from boot using a `systemd` service. This service will keep the application running, even if it fails.

### Command Line
The application can be run with the command line with:

```bash
./app.py -c <your config file.py>
```

a `-d` flag can be added for full debug logs.

**Note**: The application does not need the `install.sh` script to run. This git repo can be pulled and run with the above command (as long as all the Linux and Python requirements are met).

## Examples Projects
Below is a list of projects currently using PiMediaSync to run exhibits:

* [mini-world-sawmill-display](https://github.com/limbicmedia/mini-world-sawmill-display)