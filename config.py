import RPi.GPIO as GPIO


class Config():
    VIDEONAME = "./video/sawmill.mov"
    DMX_DEVICE = "/dev/ttyUSB0"

    GPIO_VALUES = {
        'pin': 10,
        'pull_up_down': GPIO.PUD_OFF,
        'bouncetime': 100
        }

    DEFAULT_VALUE = 255
    CHANNELS = [25, 26, 27, 22, 23, 24, 19, 20, 21, 16, 17, 18]  # order of DMX channels
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
