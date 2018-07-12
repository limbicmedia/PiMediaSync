# Miniature World Sawmill Exhibit

## Install
On a Raspberry Pi running [Linux Debian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/), run:

```
wget -O - https://raw.githubusercontent.com/limbicmedia/mini-world-sawmill-display/master/scripts/install.sh | bash
```

This will install all the necessary requirements (including downloading this git repo)

## Wiring
The button wiring is based on [this guide](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/).

This diagram shows how it is wired:

![button wiring](https://raspberrypihq.com/wp-content/uploads/2018/02/02_Push-button_bb-min.jpg)

## HDMI
### Always On
Based on [this](https://raspberrypi.stackexchange.com/questions/2169/how-do-i-force-the-raspberry-pi-to-turn-on-hdmi) post:
HDMI should always be active. In `/boot/config` add:
```
hdmi_force_hotplug=1
hdmi_drive=2
```
hdmi_force_hotplug=1 sets the Raspbmc to use HDMI mode even if no HDMI monitor is detected. hdmi_drive=2 sets the Raspbmc to normal HDMI mode (Sound will be sent if supported and enabled). Without this line, the Raspbmc would switch to DVI (with no audio) mode by default

### Always 1080p
Base on [this](https://raspberrypi.stackexchange.com/questions/10017/hdmi-output-for-1080p)
Modify `/boot/config.txt` to have:
```
hdmi_mode=16
```