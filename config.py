import RPi.GPIO as GPIO

class Config():
    VIDEONAME = "./video/SAWMILL.mp4"
    DMX_DEVICE = "/dev/ttyUSB0"
    
    GPIO_VALUES = {
        'pin': 10,
        'pull_up_down': GPIO.PUD_DOWN
        }

    DEFAULT_VALUE = 255
    CHANNELS = [25, 26, 27, 22, 23, 24, 19, 20, 21, 16] # order of DMX channels
    LIGHTING_SEQUENCE = [
        {
            'dmx_levels': [255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 5.0
        },
        {
            'dmx_levels': [0, 255, 0, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 10.0
        },
        {
            'dmx_levels': [0, 0, 255, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 15.0
        },
        {
            'dmx_levels': [0, 0, 0, 255, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 20.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 255, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 25.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 0, 255, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 30.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 0, 0, 255, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 35.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 255, 0, 0],
            'dmx_transition': 1,
            'end_time': 40.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 0, 255, 0],
            'dmx_transition': 1,
            'end_time': 45.0
        },
        {
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 255],
            'dmx_transition': 1,
            'end_time': 50.0
        },
        {
            # end
            'dmx_levels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            'dmx_transition': 1,
            'end_time': 55.0
        }
    ]
