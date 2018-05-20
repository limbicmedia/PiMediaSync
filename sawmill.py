#!/usr/bin/env python3
import subprocess
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging

#https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
def button_callback(channel):
    print("Button was pushed!")

# Get Metadata for 
def getMetadata(filename):
    ffmpeg_cmd = ["ffmpeg", "-loglevel", "panic", "-i", filename, "-f", "ffmetadata", "-"]
    meta = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE).stdout
    meta = meta.decode("utf-8")

    meta = meta.splitlines()
    # break into chunks
    # WRITE TEST!
    data = []
    index = 0
    while "[CHAPTER]" in meta[index:]:
        index += meta[index:].index("[CHAPTER]")
        index += 1
        section = meta[index:index+4]
        temp = {k:v for k,v in (x.split('=') for x in section)}
        data.append(temp)
    return data

def start(player):
    player.pause()
    player.position(0)
    player.play()


def main(filename, player_log):
    data = getMetadata(filename)

    player = OMXPlayer(filename, 
            dbus_name='org.mpris.MediaPlayer2.omxplayer1')
    player.playEvent += lambda _: player_log.info("Play")
    player.pauseEvent += lambda _: player_log.info("Pause")
    player.stopEvent += lambda _: player_log.info("Stop")
    player.pause()
    sleep(2.5)
    
    #on button press
    player.play()

    index = 0
    for steps in data:
        # set dmx value
        # calculate next postion
        next_position = eval(steps['TIMEBASE']) * int(steps['END'])
        print("index: {0}".format(index))
        print("current position: {0}".format(player.position()))
        print("next position: {0}".format(next_position))
        index += 1
        sleep(next_position - player.position())
    #player.has_track_list()
    #player.playback_status

    # values to be used for omxplayer
    #for val in data:

    #BUTTON
    # RPi.GPIO Python library now supports Events
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Does a thing to some stuff.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        "filename",
        help="filename for video to play",
        metavar="ARG")
    parser.add_argument(
        "-d",
        "--debug",
        help="increase output verbosity",
        action="store_true")
    # parser.add_argument(
    #     'remaining',
    #     help="catch all other arguments to be passed to OMXplayer",
    #     nargs=argparse.REMAINDER)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    # Setup logging
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(10, GPIO.FALLING, callback=button_callback) # Setup event on pin 10 rising edge
    
    filename = "SAWMILL_export.mp4"
    player_log = logging.getLogger("Player 1")

    try:
        main(filename, player_log)
    except as e:
        player_log.error(e)

    finally:
        GPIO.cleanup()
