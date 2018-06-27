#!/usr/bin/env python3
import argparse
from time import sleep
import logging
from threading import Event
import buttonhandler
import omxdmx
from config import Config
import RPi.GPIO as GPIO

def buttonCallback(buttonEvent):
        '''
        Simple callback to relay button press to other thread
        '''

        player_log.debug("Button Pressed")
        buttonEvent.set()

def buttonSetup(pin, event, bouncetime=10):
    '''
    Simple helper function to get all button stuff setup
    including the button callback.

    the GPIO class appears to be a singleton of sorts

    '''

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    buttoncb = lambda threadChannel, event=event: buttonCallback(event) # hack to get args into button function
    buttonHandlerCb = buttonhandler.ButtonHandler(
        pin, buttoncb, edge='falling', bouncetime=bouncetime)
    buttonHandlerCb.start()
    GPIO.add_event_detect(pin, GPIO.RISING, callback=buttonHandlerCb)


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
    args = parser.parse_args()

    # Setup logging
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
    omxDmxThread = omxdmx.OmxDmx(buttonEvent, killEvent, Config)
    
    buttonSetup(10, buttonEvent, bouncetime=100)

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