sudo apt-get update
sudo apt-get install -y git vim python3

# pySimpleDMX
# `pip3 install pysimpledmx` does not install working version
pip3 install git+https://github.com/limbicmedia/pySimpleDMX.git

git clone https://github.com/limbicmedia/mini-world-sawmill-display
pip3 install -r ./mini-world-sawmill-display/requirements.txt
sudo chmod u+x ./mini-world-sawmill-display/sawmill.py

# SystemD Setup
sudo systemctl enable ./mini-world-sawmill-display/scripts/mini-world-sawmill-display.service

# install alsa default file for audio levels?