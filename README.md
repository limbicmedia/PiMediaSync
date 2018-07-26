# Miniature World Sawmill Exhibit

## Install
On a Raspberry Pi running [Linux Debian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/), run:

```
wget -O - https://raw.githubusercontent.com/limbicmedia/mini-world-sawmill-display/master/scripts/install.sh | bash
```

This will install all the necessary requirements (including downloading this git repo)

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