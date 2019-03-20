import RPi.GPIO as GPIO

class Config():
    '''
    Example Config file for use in MediaSync application
    '''

    # OPTIONAL; location and filename of mediafile for playing (uses OMXPlayer to play). 
    # If none provided (or incorrect provided), creates fake virtual device
    VIDEONAME = "./video/sawmill.mov"

    # OPTIONAL; Enttec serial device for DMX output. 
    #If none provided (or incorrect provided), creates fake virtual device
    DMX_DEVICE = "/dev/ttyUSB0"

    # OPTIONAL; BUTTON setup values
    GPIO_VALUES = {
        'pin': 10,
        'pull_up_down': GPIO.PUD_OFF,
    }

    SCHEDULER_TIME = 10 # OPTIONAL; causes automatic start of sequence via scheduled "virtual" button press

    AUTOREPEAT=False # OPTIONAL; True causes automatic start and repeat of media sequence. Defaults to False if not defined

    DEFAULT_VALUE = 255 # REQUIRED; the default value of ALL DMX channels at start.
    DEFAULT_TRANSITION_TIME = 0 # REQUIRED; the default transition time at beginning and end of sequence (bookends LIGHTING_SEQUENCE below)

    # REQUIRED; the DMX channel mapping, i.e. the order of the DMX channels in the LIGHTING_SEQUENCE below
    CHANNELS = [25, 26, 27, 22, 23, 24, 19, 20, 21, 16, 17, 18]

    # REQUIRED: the sequence of DMX light levels, essentially a playlist of DMX states. Uses CHANNELS (above) for channel order mapping
    LIGHTING_SEQUENCE = [
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 65
        },
        {
            'dmx_levels': [255, 22, 22, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 98
        },
        {
            'dmx_levels': [22, 255, 22, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 117
        },
        {
            'dmx_levels': [22, 22, 255, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 137
        },
        {
            'dmx_levels': [22, 22, 22, 255, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 159
        },
        {
            'dmx_levels': [22, 22, 22, 22, 255, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 189
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 255, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 253
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 255, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 287
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 255, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 315
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 22, 255, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 327
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 22, 22, 255, 0, 0],
            'dmx_transition': 1,
            'end_time': 357
        },
        {
            # end
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 372
        }
    ]
