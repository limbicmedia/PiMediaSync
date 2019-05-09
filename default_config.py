class Config():
    '''
    Default config file used in PyMediaSync application

    This file sets the default state of all config file attributes. 
    This allows sparse config files to be used, only requring the user 
    to set relevant attributes in their config file (i.e. not all attributes 
    have to be set in external config files)
    '''

    # location and filename of mediafile for playing (uses OMXPlayer to play). 
    # If none provided (or incorrect provided), creates fake virtual device
    MEDIA_NAME = None

    # Enttec serial device for DMX output. 
    # If none provided (or incorrect provided), creates fake virtual device
    DMX_DEVICE = "/dev/null"

    # BUTTON setup values
    # If none provided, no GPIO input is used
    GPIO_VALUES = {
        'pin': None,
        'pull_up_down': None,
    }

    # causes automatic start of sequence via scheduled "virtual" button press
    # if set to '0', scheduler does not run
    SCHEDULER_TIME = 0

    AUTOREPEAT = False  # True causes automatic start and repeat of media sequence. Defaults to False if not defined
    AUTOREPEAT_TOGGLE = { # Adds a gpio pin to read a toggle switch on startup to enable/disable AUTOREPEAT. NOTE: overrides AUTOREPEAT variable above
        'gpio_pin': None
    }

    DEFAULT_VALUE = 255  # the default value of ALL DMX channels at start.
    DEFAULT_TRANSITION_TIME = 0  # the default transition time at beginning and end of sequence (bookends LIGHTING_SEQUENCE below)

    # the DMX channel mapping, i.e. the order of the DMX channels in the LIGHTING_SEQUENCE below
    CHANNELS = [1]

    # the sequence of DMX light levels, essentially a playlist of DMX states. Uses CHANNELS (above) for channel order mapping
    LIGHTING_SEQUENCE = []
