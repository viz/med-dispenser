# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import asyncio
import board
import digitalio
import keypad
import displayio
import busio
import neopixel
import adafruit_pcf8563
import time
import adafruit_displayio_ssd1306
from adafruit_display_text import label

WIDTH = 128
HEIGHT = 64
CENTER_X = int(WIDTH/2)
CENTER_Y = int(HEIGHT/2)
SDA = board.SDA
SCL = board.SCL

displayio.release_displays()

async def update_status(interval):  # Don't forget the async!
    while True:
        print("sending status to webservice")
        await asyncio.sleep(interval)  # Don't forget the await!

async def illuminate_cell(pixels):  # Don't forget the async!
    while True:
        pixels[0] = (0,100,0)
        await asyncio.sleep(interval)  # Don't forget the await!


async def check_buttons(rtc, pin_ack):  # Don't forget the async!
    # Assume buttons are active low.
    with keypad.Keys(
        (pin_ack,), value_when_pressed=False, pull=True
    ) as keys:
        while True:
            key_event = keys.events.get()
            if key_event and key_event.pressed:
                if key_event.key_number == 0:

                    print("alert acknowledged " )
                else:
                    print("something else happened")
            # Let another task run.
            await asyncio.sleep(0)


async def main():  # Don't forget the async!
    i2c = busio.I2C(SCL, SDA)
    if(i2c.try_lock()):
        print("i2c.scan(): " + str(i2c.scan()))
        i2c.unlock()
    
    rtc = adafruit_pcf8563.PCF8563(i2c)
    rtc.datetime = time.struct_time((2023,1,7,17,0,0,5,-1,1))
    currTime = rtc.datetime
    print("time is: ", currTime.tm_sec)
    display_bus = displayio.I2CDisplay(i2c, device_address=60)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    pixels = neopixel.NeoPixel(board.D0, 15)

    status_update_task = asyncio.create_task(update_status(5))
    check_button_task = asyncio.create_task(check_buttons(rtc, board.D1))
    await asyncio.gather(status_update_task, check_button_task)  # Don't forget the await!
    print("done")


asyncio.run(main())
