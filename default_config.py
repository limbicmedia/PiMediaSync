class Config():
    '''
    Example Config file for use in MediaSync application
    '''

    # OPTIONAL; location and filename of mediafile for playing (uses OMXPlayer to play). 
    # If none provided (or incorrect provided), creates fake virtual device
    VIDEONAME = None

    # OPTIONAL; Enttec serial device for DMX output. 
    # If none provided (or incorrect provided), creates fake virtual device
    DMX_DEVICE = "/dev/null"

    # OPTIONAL; BUTTON setup values
    GPIO_VALUES = {
        'pin': None,
        'pull_up_down': None,
    }

    SCHEDULER_TIME = 0  # OPTIONAL; causes automatic start of sequence via scheduled "virtual" button press

    AUTOREPEAT = False  # OPTIONAL; True causes automatic start and repeat of media sequence. Defaults to False if not defined

    DEFAULT_VALUE = 255  # REQUIRED; the default value of ALL DMX channels at start.
    DEFAULT_TRANSITION_TIME = 0  # REQUIRED; the default transition time at beginning and end of sequence (bookends LIGHTING_SEQUENCE below)

    # REQUIRED; the DMX channel mapping, i.e. the order of the DMX channels in the LIGHTING_SEQUENCE below
    CHANNELS = [1]

    # REQUIRED: the sequence of DMX light levels, essentially a playlist of DMX states. Uses CHANNELS (above) for channel order mapping
    LIGHTING_SEQUENCE = []
