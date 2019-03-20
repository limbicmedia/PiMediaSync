#!/usr/bin/env bash
set -e
if [ "$(whoami)" != "root" ]; then
    echo "must be run as root."
    exit 1
fi

HOMEDIR="${HOMEDIR:-/opt}"
cd $HOMEDIR

PIHOSTNAME="${PIHOSTNAME:-pimediasync}"
echo "Setting HOSTNAME to $PIHOSTNAME"
echo "$PIHOSTNAME" > /etc/hostname

apt-get update
apt-get install --no-install-recommends -y \
    git \
    vim \
    omxplayer \
    python3 \
    python3-pip \
    python3-dbus \
    python3-setuptools
apt-get clean

# pySimpleDMX
# `pip3 install pysimpledmx` does not install working version
PYSIMPLEDMX_VERSION="v0.2.0"
pip3 install git+https://github.com/limbicmedia/pySimpleDMX.git@${PYSIMPLEDMX_VERSION}

git clone https://github.com/limbicmedia/pimediasync
pip3 install -r ${HOMEDIR}/PiMediaSync/requirements.txt
chmod u+x ${HOMEDIR}/PiMediaSync/app.py

# SystemD Setup
systemctl enable ${HOMEDIR}/PiMediaSync/scripts/pimediasync.service

# Display Setup
echo "hdmi_force_hotplug=1" >> /boot/config.txt # HDMI mode even if no HDMI monitor is detected
echo "hdmi_drive=2" >> /boot/config.txt # normal HDMI mode
echo "hdmi_mode=16" >> /boot/config.txt # Always 1080p HDMI output

if [ -z "$DEBUG" ]; then 
    # set log directory to be TMPFS;
    echo "tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0    0" >> /etc/fstab
fi
set +e