from threading import Event, Thread
import logging
from time import sleep

from config import Config
from omxplayer.player import OMXPlayer, OMXPlayerDeadError
import pysimpledmx

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

class OmxDmx(Thread):
    def __init__(self, buttonEvent, killEvent, numChannels, Config):
        super().__init__()
        self.logger = logging.getLogger("omxdmx")
        self.buttonEvent = buttonEvent
        self.killEvent = killEvent

        self.player = self.playerFactory(Config.VIDEONAME, self.logger)
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
        we desire
        '''

        player = OMXPlayer(filename, 
                dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['-b', '-o', 'both'])
        player.playEvent += lambda _: logger.debug("Play")
        player.pauseEvent += lambda _: logger.debug("Pause")
        player.stopEvent += lambda _: logger.debug("Stop")
        
        while True:
            try:
                print("hiding video")
                player.hide_video()
                print("pausing video")
                player.pause()
                break
            except Exception as e:
                logger.exception("Exception in playerFactory")
                sys.exit(1)
        return player