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
            'end_time': 66
        },
        {
            'dmx_levels': [255, 22, 22, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 99
        },
        {
            'dmx_levels': [22, 255, 22, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 118
        },
        {
            'dmx_levels': [22, 22, 255, 22, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 138
        },
        {
            'dmx_levels': [22, 22, 22, 255, 22, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 160
        },
        {
            'dmx_levels': [22, 22, 22, 22, 255, 22, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 190
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 255, 22, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 254
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 255, 22, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 288
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 255, 22, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 316
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 22, 255, 22, 0, 0],
            'dmx_transition': 1,
            'end_time': 328
        },
        {
            'dmx_levels': [22, 22, 22, 22, 22, 22, 22, 22, 22, 255, 0, 0],
            'dmx_transition': 1,
            'end_time': 358
        },
        {
            # end
            'dmx_levels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'dmx_transition': 1,
            'end_time': 381
        }
    ]
