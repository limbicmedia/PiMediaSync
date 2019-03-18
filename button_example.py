import RPi.GPIO as GPIO
import logging
'''
Button Example Code

The code below shows an example setup for handling buttons interfacing with the Raspberry Pi
via GPIOs. This is effectively how buttons are setup in the main of this software.

Run this code on a Raspberry PI to test the button action.

Note: The button is expected to have a 1uf capacitor to assist with button debouncing. This will reduce the 
instances of multiple hits but it is not 100% effective.

In the main of this project, 'events' are used to capture button presses and those act as a simple filter
for multiple presses (since an event can only be `set()` once for an observable change).
'''
if __name__ == '__main__':
    from time import sleep
    
    def increase_press_count(*args):
        global COUNT
        COUNT += 1
        print("Button Pressed: {}".format(COUNT))

    COUNT = 0
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    buttoncb = lambda threadChannel: increase_press_count() # hack to get args into button function
    GPIO.add_event_detect(10, GPIO.RISING, callback=buttoncb)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, cleaning up GPIO")
        GPIO.cleanup()
    finally:
        print("finished")


