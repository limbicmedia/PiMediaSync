#!/usr/bin/env bash
if [ "$(whoami)" != "root" ]; then
    echo "must be run as root."
    exit 1
fi

HOMEDIR="${HOMEDIR:-/root}"
cd $HOMEDIR

PIHOSTNAME="${PIHOSTNAME:-miniworld-sawmill}"
echo "Setting HOSTNAME to $PIHOSTNAME"
echo "$PIHOSTNAME" > /etc/hostname

apt-get update
apt-get install -y git vim python3 python3-pip omxplayer
apt-get clean

# pySimpleDMX
# `pip3 install pysimpledmx` does not install working version
pip3 install git+https://github.com/limbicmedia/pySimpleDMX.git

git clone https://github.com/limbicmedia/mini-world-sawmill-display
pip3 install -r /root/mini-world-sawmill-display/requirements.txt
chmod u+x /root/mini-world-sawmill-display/sawmill.py

# SystemD Setup
systemctl enable /root/mini-world-sawmill-display/scripts/sawmill.service

# install alsa default file for audio levels?

if [ -z "$DEBUG" ]; then 
    # set log directory to be TMPFS;
    echo "tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0    0" >> /etc/fstab
fi