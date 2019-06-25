import sys
import os
from threading import Event, Thread
import logging
from time import sleep
from datetime import datetime
from omxplayer.player import OMXPlayer, OMXPlayerDeadError
import pysimpledmx

# neeeded for omxPlayerMock
import evento

# globals
END_DURATION_OFFSET = .25  # if no SEQUENCE defined, this variable sets how far from the end of the media file to automatically stop playing

class dmxFake(pysimpledmx.DMXConnection):
    '''
    Used when actual DMX serial device is unavailable
    '''
    def __init__(self):
        self.logger = logging.getLogger("dmxFake")
        self.logger.info("Mock DMX class initiated")

    def ramp(self, channels, steps, duration):
        self.logger.info("Mock DMX ramp method")
        mix = list(zip(channels, steps))
        self.logger.info("Channels and Steps: {}".format(mix))
        self.logger.info("Duration: {}".format(duration))


class omxPlayerMock():
    '''
    Mock class for instantiating when a video/audio file is not available

    The idea is to keep all code pertaining to omxPlayer while allowing
    for instances of OmxDmx without an actual OMXPlayer.
    '''

    def __init__(self, filename):
        self.logger = logging.getLogger("omxPlayerMock")
        self.logger.info("Mock OMXPlayer class initiated")

        self.pauseEvent = evento.event.Event()
        self.playEvent = evento.event.Event()
        self.stopEvent = evento.event.Event()
        self.exitEvent = evento.event.Event()
        self.seekEvent = evento.event.Event()
        self.positionEvent = evento.event.Event()

        self.playbackStatus = "Stopped"  # ("Playing" | "Paused" | "Stopped")
        self.start_time = datetime.utcnow() # keep track of when mock system started "playing"

    def hide_video(self):
        pass

    def pause(self):
        self.playbackStatus = "Paused"
        self.pauseEvent(self)

    def play(self):
        self.playbackStatus = "Playing"
        self.start_time = datetime.utcnow()
        self.logger.debug("start_time = {0}".format(self.start_time.timestamp()))
        self.playEvent(self)

    def position(self):
        current_position = float((datetime.utcnow() - self.start_time).total_seconds())
        self.logger.debug("current_position = {0}".format(current_position))
        return current_position

    def stop(self):
        self.playbackStatus = "Stopped"
        self.stopEvent(self)

    def exit(self):
        self.exitEvent(self)

    def seek(self, val):
        self.seekEvent(self)

    def playback_status(self):
        return self.playbackStatus

    def show_video(self):
        pass

    def duration(self):
        return (sys.maxsize)  # always greater than position()

    def quit(self):
        pass


class OmxDmx(Thread):
    def __init__(self, buttonEvent, killEvent, mediafile=None, dmxDevice="/dev/null", autorepeat=False, dmxChannels=[1], dmxDefaultVals=255, defaultTransition_t=0, sequence=[]):
        super().__init__()
        self.logger = logging.getLogger("omxdmx")
        self.buttonEvent = buttonEvent
        self.killEvent = killEvent

        self.mediafile = mediafile

        self.player = self.playerFactory(self.mediafile, self.logger)

        # Automatically start and restart after end of sequence
        self.autorepeat = autorepeat
        if self.autorepeat:
            self.buttonEvent.set()

        self.dmxChannels = dmxChannels

        if(type(dmxDefaultVals) == type(list())):
            self.dmxDefaultVals = dmxDefaultVals
        else:
            self.dmxDefaultVals = [dmxDefaultVals] * len(self.dmxChannels)
        self.dmxDefaultVals += [0] * (len(self.dmxChannels)-len(self.dmxDefaultVals))  # extend if too short
        self.dmxDefaultVals = self.dmxDefaultVals[:len(self.dmxChannels)] # cut if too long

        self.defaultTransition_t = defaultTransition_t
        self.isDefault = False

        self.sequence = sequence
        if not len(self.sequence):
            self.sequence.append({
                'dmx_levels': self.dmxDefaultVals,
                'dmx_transition': self.defaultTransition_t,
                'end_time': self.player.duration() - END_DURATION_OFFSET
                })

        # setup DMX device
        self.numChannels = max(self.dmxChannels) + 1
        try:
            self.dmx = pysimpledmx.DMXConnection(dmxDevice,
                softfail=True, numChannels=self.numChannels)
        except Exception as e:
            self.logger.exception("DMX device failure, creating mock device")
            self.dmx = dmxFake()

        self.dmx.ramp(self.dmxChannels,
                self.dmxDefaultVals,
                self.defaultTransition_t)
        self.DMXisDefault = True

        # set state before run
        self.running = True
        self.playing = False

    def run(self):
        '''
        Main video playing function.
        Will run until KeyboardInterrupt or catastrophic failure.
        '''

        self.logger.debug("Waiting for video")
        while self.running:
            if(self.buttonEvent.is_set()):
                self.playing = True
                self.logger.debug("Starting Video")
            elif not self.DMXisDefault:
                # if "button" is not pressed, go to default
                self.dmx.ramp(self.dmxChannels,
                    self.dmxDefaultVals,
                    self.defaultTransition_t)
                self.DMXisDefault = True
                self.logger.debug("Button not pushed, setting lights to default values")

            if(self.killEvent.is_set()):
                self.killThread()
                break

            while self.playing:
                # make sure OMXPlayer still exists
                try:
                    self.player.playback_status()
                except OMXPlayerDeadError as e:
                    self.logger.exception("OMXPlayer has died. Exiting")
                    sys.exit(1)

                self.playFromBeginning()
                for steps in self.sequence:
                    try:
                        self.player.playback_status()
                    except OMXPlayerDeadError as e:
                        self.logger.exception("OMXPlayer has died. Exiting")
                        sys.exit(1)

                    # OMXPlayer exits if the whole video plays.
                    self.logger.debug("player at position: {}".format(self.player.position()))

                    end_check = (self.player.duration() - steps['end_time'])
                    if((self.player.duration() - steps['end_time']) < END_DURATION_OFFSET):
                        self.logger.warning("Media file is shorter than LIGHTING_SEQUENCE. Stopping video to keep application alive.")
                        self.player.pause()
                        self.player.hide_video()
                        self.playing = False
                        break

                    # handle DMX
                    self.dmx.ramp(self.dmxChannels, steps['dmx_levels'], steps['dmx_transition'])

                    sleeptime = steps['end_time'] - self.player.position()
                    # exit thread on kill event
                    if(self.killEvent.wait(sleeptime)):
                        self.killThread()
                        break

                self.DMXisDefault = False
                self.buttonEvent.clear()
                self.player.pause()
                self.player.hide_video()
                self.playing = False

                if self.autorepeat:
                    self.buttonEvent.set()

        self.player.quit()

    def killThread(self):
        '''
        Method used to kill thread once
        self.killEvent event is set
        '''
        self.logger.debug("kill event received, killing app")
        self.running = False
        self.killEvent.clear()

    def playFromBeginning(self):
        '''
        Simple wrapper for playing from start.
        Could extend omxplayer class...
        '''

        self.player.seek(-(self.player.position() + .5))  # player to "beginning"
        sleep(.1)
        self.player.play()
        sleep(.5)
        self.player.show_video()

    @staticmethod
    def playerFactory(filename, logger):
        '''
        Creates an instance of OMXPlayer the starting state
        we desire.

        If filename does not exist (or is None), generates a Mock devices
        with equivalent functionality (but no media output)
        '''

        if filename is not None and not os.path.isfile(filename):
            logger.warning("Media file: {} DOES NOT EXIST".format(filename))
            filename = None # force try to fail quickly below

        try:
            player = OMXPlayer(filename,
                    dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['-b', '-o', 'both'])
        except Exception as e:
            player = omxPlayerMock(filename);

        player.playEvent += lambda _: logger.debug("Play")
        player.pauseEvent += lambda _: logger.debug("Pause")
        player.stopEvent += lambda _: logger.debug("Stop")

        while True:
            try:
                player.hide_video()
                player.pause()
                break
            except Exception as e:
                logger.exception("Exception in playerFactory")
                sys.exit(1)
        return player


class RepeatScheduler(Thread):
    '''
    RepeatScheduler is a threaded scheduler for excuting a callback on a
    repeated interval
    '''
    def __init__(self, repeatTime, killEvent, callback=None, callbackArgs=()):
        Thread.__init__(self)
        self.logger = logging.getLogger("RepeatScheduler")
        self.logger.info("RepeatScheduler activated with \
            callback: {}".format(callback))

        self.killEvent = killEvent
        self.repeatTime = repeatTime
        self.callback = callback
        self.callbackArgs = callbackArgs

    def run(self):
        while not self.killEvent.wait(self.repeatTime):
            self.logger.debug("RepeatScheduler ran after waiting \
                for {} seconds".format(self.repeatTime))
            if self.callback is not None:
                self.callback(*self.callbackArgs)
        self.logger.debug("Thread exiting.")


if __name__ == '__main__':
    def increase_press_count():
        global COUNT
        COUNT += 1
        print("RepeatScheduler count: {}".format(COUNT))

    repeatTime = .1 # 1 second delay between
    killEvent = Event()
    COUNT = 0

    t = RepeatScheduler(repeatTime, killEvent, callback=increase_press_count)
    t.start()

    while(COUNT < 5):
        sleep(repeatTime)

    killEvent.set()