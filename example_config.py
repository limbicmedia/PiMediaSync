import RPi.GPIO as GPIO # required for GPIO configuration

class Config():
    MEDIA_NAME = "./video/myvideo.mov" # ./ is relative to PiMediaSync repo
    DMX_DEVICE = "/dev/ttyUSB0". # the DMX device

    # configure button input on pin 10 with no internal pull up/down resistor
    GPIO_VALUES = {
        'pin': 10,
        'pull_up_down': GPIO.PUD_OFF,
    }
    
    SCHEDULER_TIME = 600 # activate sequence automatically every 10 minutes

    AUTOREPEAT=False # auto repeat disabled

    DEFAULT_VALUE = 255 # DMX lights start/stop on brightness of 255
    DEFAULT_TRANSITION_TIME = 1 # DMX lights start/stop with transition time of 1 second
    CHANNELS = [1, 4, 3, 2, 5] # DMX light channel mapping order -- notice they can be any order
    LIGHTING_SEQUENCE = [
        {
            'dmx_levels': [0, 0, 0, 0, 0], # set all DMX outputs to 0
            'dmx_transition': 5, # take 5 seconds to transition to dmx_levels
            'end_time': 10 # after 10 second, move to the next sequence
        },
        {
            'dmx_levels': [0, 255, 0, 0, 0], # set DMX output channel 4 to 255
            'dmx_transition': 10,  # take 10 seconds to transition to dmx_levels
            'end_time': 60 # after 60 second, move to the next sequence
            # done, return to the beginning of sequence, set `DEFAULT_VALUE` and pause.
        }
    ]