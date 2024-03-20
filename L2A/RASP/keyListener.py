import os
import usb_cdc

import time
import random

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
while True:
    buf = usb_cdc.data.read(1)
    #usb_cdc.data.reset_input_buffer()
    #randTime = (random.randint(1, 100)) / 1000
    #time.sleep(randTime)  # Sleep for a bit to avoid a race condition on some systems
    #print("key pressed: ", buf[0])
    keyboard.press(buf[0])
    randTime = (random.randint(1, 30)) / 1000
    time.sleep(randTime)
    keyboard.release_all()