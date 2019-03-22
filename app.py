#!/usr/bin/env python3
import argparse, sys, os, logging
import subprocess, signal
from time import sleep
from threading import Event
import omxdmx
import RPi.GPIO as GPIO

from flask.config import Config as fConfig
import default_config

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

def killProcess(processName):
    '''
    Kills Linux processes by name
    '''
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if processName in str(line):
            pid = int(line.split(None, 1)[0])
            player_log.debug("Rogue process: {0} with PID: {1} found. Killing.".format(processName, pid))
            os.kill(pid, signal.SIGKILL)
            player_log.debug("Rogue process: {0} with PID: {1} killed.".format(processName, pid))


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
        help="set config filename and directory.")
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

    # generate application config
    config = fConfig("./")
    config.from_object(default_config.Config)  # load defaults

    # would try to import with `from_pyfile()` but doesn't work for this format 
    if(args.config):
        directory, module_name = os.path.split(args.config)
        module_name = os.path.splitext(module_name)[0]
        path = list(sys.path)
        sys.path.insert(0, directory)
        
        try:
            module = __import__(module_name)
            config.from_object(module.Config)
        finally:
            sys.path[:] = path # restore

    # removed any leftover omxplayer processes
    killProcess("omxplayer")

    buttonEvent = Event()
    omxKillEvent = Event()

    # flag for informing if application can ever activate
    hasActivationInput = False

    # attempt setup of "virtual" button on timer
    schedulerKillEvent = Event()  # used later, even if not connected
    schedule_t = config['SCHEDULER_TIME']
    if (schedule_t > 0):
        scheduledButton = omxdmx.RepeatScheduler(schedule_t, schedulerKillEvent,
            callback=lambda event=buttonEvent: buttonCallback(event))
        scheduledButton.start()
        hasActivationInput = True
        player_log.info("Scheduler enabled with {} second timer.".format(schedule_t))
    else:
        player_log.info("Scheduler disabled because SCHEDULER_TIME set to {}.".format(schedule_t))

    # Attempt to setup user input (button)
    gpio_values = config['GPIO_VALUES']
    if gpio_values['pin'] and gpio_values['pull_up_down']:
        buttonSetup(gpio_values['pin'],
            gpio_values['pull_up_down'],
            buttonEvent)
        hasActivationInput = True
        player_log.info("Button enabled on pin {}.".format(gpio_values['pin']))
    else:
        player_log.info("Button not enabled.".format())

    if not hasActivationInput and not config['AUTOREPEAT']:
        player_log.info("No user input--button or timer--set and AUTOREPEAT is False. Program will sit and do nothing.")

    omxDmxThread = omxdmx.OmxDmx(buttonEvent, omxKillEvent,
                        mediafile=config['VIDEONAME'],
                        autorepeat=config['AUTOREPEAT'],
                        dmxDevice=config["DMX_DEVICE"],
                        dmxChannels=config['CHANNELS'],
                        dmxDefaultVals=config['DEFAULT_VALUE'],
                        defaultTransition_t=config['DEFAULT_TRANSITION_TIME'],
                        sequence=config['LIGHTING_SEQUENCE'])

    try:
        omxDmxThread.start()
        omxDmxThread.join()
    except KeyboardInterrupt as e:
        player_log.exception("KeyboardInterrupt")
        schedulerKillEvent.set()
        omxKillEvent.set()
        while(omxDmxThread.isAlive()):
            player_log.debug("waiting for thread to quit")
            sleep(1)
    except SystemExit as e:
        player_log.exception("SystemExit")
        schedulerKillEvent.set()
        omxKillEvent.set()
        while(omxDmxThread.isAlive()):
            player_log.debug("waiting for thread to quit")
            sleep(1)
    finally:
        GPIO.cleanup()
