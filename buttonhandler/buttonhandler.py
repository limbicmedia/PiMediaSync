import RPi.GPIO as GPIO
import threading
import logging

# based on this code:
# https://raspberrypi.stackexchange.com/questions/76667/debouncing-buttons-with-rpi-gpio-too-many-events-detected

class ButtonHandler(threading.Thread):
    def __init__(self, pin, cb, edge='both', bouncetime=200):
        super().__init__(daemon=True)
        self.logger = logging.getLogger('buttonhandler')
        self.edge = edge
        self.cb = cb
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.cb(*args)

        self.lastpinval = pinval
        self.lock.release()

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
    cb = ButtonHandler(10, real_cb, edge='falling', bouncetime=10)
    cb.start()
    GPIO.add_event_detect(10, GPIO.RISING, callback=cb)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, cleaning up GPIO")
        GPIO.cleanup()
    finally:
        print("finished")


