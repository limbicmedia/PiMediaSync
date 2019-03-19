#!/usr/bin/env python3
import argparse, sys, os, logging
from time import sleep
from threading import Event
import omxdmx
import RPi.GPIO as GPIO

def buttonCallback(buttonEvent):
        '''
        Simple callback to relay button press to other thread
        '''

        player_log.debug("Button Pressed")
        buttonEvent.set()

def buttonSetup(pin, pull_up_down, event):
    '''
    Simple helper function to get all button stuff setup
    including the button callback.

    the GPIO class appears to be a singleton of sorts

    '''

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)

    buttoncb = lambda threadChannel, event=event: buttonCallback(event) # hack to get args into button function
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=buttoncb)

def loadConfig(configLocation, moduleName="Config"):
    '''
    Dynamically loads config file as a module.
    This allows for config files with any filename
    and location to be loaded.
    '''
    config_path, config_file = os.path.split(args.config)
    config_file = os.path.splitext(config_file)[0]

    # adds config directory to sys.path
    sys.path.append(config_path)

    # allows specified config file name
    config = __import__(config_file)
    Config = getattr(config, moduleName)

    return Config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Syncronizes video and dmx lighting \
        sequences on a Raspberry Pi using OMXPlayer and \
        and Enttec USB-to-DMX converter.")
    parser.add_argument(
        "-d",
        "--debug",
        help="increase output verbosity",
        action="store_true")
    parser.add_argument(
        "-c",
        "--config",
        help="set config filename and directory.",
        default="./config.py")
    args = parser.parse_args()

    Config = loadConfig(args.config)

    ## Setup logging
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    player_log = logging.getLogger("sawmill")
    logging.basicConfig(
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p', 
        level=loglevel)

    killEvent = Event()
    buttonEvent = Event()
    num_channels = max(Config.CHANNELS) + 1
    omxDmxThread = omxdmx.OmxDmx(buttonEvent, killEvent, num_channels, Config)
    
    buttonSetup(Config.GPIO_VALUES['pin'], Config.GPIO_VALUES['pull_up_down'], 
        buttonEvent)

    try:
        omxDmxThread.start()
        omxDmxThread.join()
    except KeyboardInterrupt as e:
        player_log.exception("KeyboardInterrupt")
        killEvent.set()
        while(omxDmxThread.isAlive()):
            player_log.debug("waiting for thread to quit")
            sleep(1)
    except SystemExit as e:
        player_log.exception("SystemExit")
        killEvent.set()
        while(omxDmxThread.isAlive()):
            player_log.debug("waiting for thread to quit")
            sleep(1)
    finally:
        GPIO.cleanup()
