import RPi.GPIO as GPIO

class Config():
    VIDEONAME = "./video/sawmill.mov"
    DMX_DEVICE = "/dev/ttyUSB0"
    
    GPIO_VALUES = {
        'pin': 10,
        'pull_up_down': GPIO.PUD_OFF
        'bouncetime': 100
        }

    DEFAULT_VALUE = 255
    CHANNELS = [25, 26, 27, 22, 23, 24, 19, 20, 21, 16, 17, 18] # order of DMX channels
    LIGHTING_SEQUENCE = [
        {
            'dmx_levels': [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 68
        },
        {
            'dmx_levels': [255, 64, 64, 64, 64, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 92
        },
        {
            'dmx_levels': [64, 255, 64, 64, 64, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 120
        },
        {
            'dmx_levels': [64, 64, 255, 64, 64, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 140
        },
        {
            'dmx_levels': [64, 64, 64, 255, 64, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 162
        },
        {
            'dmx_levels': [64, 64, 64, 64, 255, 64, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 192
        },
        {
            'dmx_levels': [64, 64, 64, 64, 64, 255, 64, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 256
        },
        {
            'dmx_levels': [64, 64, 64, 64, 64, 64, 255, 64, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 290
        },
        {
            'dmx_levels': [64, 64, 64, 64, 64, 64, 64, 255, 64, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 318
        },
        {
            'dmx_levels': [64, 64, 64, 64, 64, 64, 64, 64, 255, 64, 0, 0],
            'dmx_transition': 1,
            'end_time': 330
        },
        {
            'dmx_levels': [64, 64, 64, 64, 64, 64, 64, 64, 64, 255, 0, 0],
            'dmx_transition': 1,
            'end_time': 360
        },
        {
            # end
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 381
        }
    ]
