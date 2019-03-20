import sys, os
from threading import Event, Thread
import logging
from time import sleep
from omxplayer.player import OMXPlayer, OMXPlayerDeadError
import pysimpledmx

# neeeded for omxPlayerMock
import evento

class dmxMock(pysimpledmx.DMXConnection):
    '''
    Used when actual DMX serial device is unavailable
    '''
    def __init__(self):
        self.logger = logging.getLogger("dmxMock")
        self.logger.info("Mock DMX class initiated")
    def ramp(self, channels, steps, duration):
        self.logger.info("Mock DMX ramp method")
        mix = list(zip(channels, steps))
        self.logger.info("Channels and Steps: {}".format(mix))
        self.logger.info("Duration: {}".format(duration))

class omxPlayerMock():
    '''
    Mock class for instantiating when a video/audio file is not available

    The idea is to keep all code pertaining to omxPlayer while allowing for instances of
    OmxDmx without an actual OMXPlayer.
    '''

    def __init__(self, filename):
        self.logger = logging.getLogger("omxPlayerMock")
        self.logger.info("Mock OMXPlayer class initiated")

        ## All events in this step are 
        self.pauseEvent = evento.event.Event()
        self.playEvent = evento.event.Event()
        self.stopEvent = evento.event.Event()
        self.exitEvent = evento.event.Event()
        self.seekEvent = evento.event.Event()
        self.positionEvent = evento.event.Event()

        self.playbackStatus = "Stopped" #("Playing" | "Paused" | "Stopped")

    def hide_video(self):
        pass

    def pause(self):
        self.playbackStatus = "Paused"
        self.pauseEvent(self)

    def play(self):
        self.playbackStatus = "Playing"
        self.playEvent(self)

    def position(self):
        return 0

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
        return (self.position() + 1) # always needs to be greater than position()

    def quit(self):
        pass


class OmxDmx(Thread):
    def __init__(self, buttonEvent, killEvent, numChannels, Config):
        super().__init__()
        self.logger = logging.getLogger("omxdmx")
        self.buttonEvent = buttonEvent
        self.killEvent = killEvent

        try:
            self.mediafile = Config.VIDEONAME
        except:
            self.mediafile = None

        self.player = self.playerFactory(self.mediafile, self.logger)
        self.sequence = Config.LIGHTING_SEQUENCE

        self.running = True
        self.playing = False

        try:
            self.dmx = pysimpledmx.DMXConnection(Config.DMX_DEVICE, softfail=True, numChannels=numChannels)
        except Exception as e:
            self.logger.exception("DMX device failure, creating mock device")
            self.dmx = dmxMock()

        # turn all lights on at start
        self.dmxChannels = Config.CHANNELS
        self.dmxDefaultVals = [Config.DEFAULT_VALUE] * len(self.dmxChannels)
        self.dmx.ramp(self.dmxChannels, self.dmxDefaultVals, 1)

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
                    if(self.player.position() > (self.player.duration() - 1)):
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
                
                self.dmx.ramp(self.dmxChannels, self.dmxDefaultVals, 1)
                
                self.buttonEvent.clear()
                self.player.pause()
                self.player.hide_video()
                self.playing = False

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

        self.player.seek(-(self.player.position() + .5)) # player to "beginning"
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

        if filename is not None and not os.path.isfile('filename'):
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
    RepeatScheduler is a threaded scheduler for excuting a callback on a repeated interval
    '''
    def __init__(self, repeatTime, killEvent, callback=None, callbackArgs=()):
        Thread.__init__(self)
        self.logger = logging.getLogger("RepeatScheduler")
        self.logger.info("RepeatScheduler activated with callback: {}".format(callback))
        
        self.killEvent = killEvent
        self.repeatTime = repeatTime
        self.callback = callback
        self.callbackArgs = callbackArgs

    def run(self):
        while not self.killEvent.wait(self.repeatTime):
            self.logger.debug("RepeatScheduler ran after waiting for {} seconds".format(self.repeatTime))
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