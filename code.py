import time
import board
import random
import asyncio
import neopixel
import digitalio
from adafruit_debouncer import Button


pixel_pin = board.D1
num_pixels = 144
buffer = 20

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, brightness=0.3)

color_pairs = [
    ((255, 0, 0), (150, 0, 0)),  # Red
    ((0, 255, 0), (0, 150, 0)),  # Green
    ((0, 0, 255), (0, 0, 150)),  # Blue
    ((255, 255, 0), (150, 150, 0)),  # Yellow
    ((0, 255, 255), (0, 150, 150)),  # Cyan
    ((255, 0, 255), (150, 0, 150))  # Magenta
]

color_ind = 0

pin = digitalio.DigitalInOut(board.D2)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP

switch = Button(pin, 1000, 3000, False)

async def pulsating_light():
    global color_ind
    while True:
        main_color, pulse_color = color_pairs[color_ind]
        for i in range(0, num_pixels+buffer):
            if i<num_pixels:
                pixels[i] = pulse_color
            if i>=buffer:
                pixels[i-buffer] = main_color
            pixels.show()
            await asyncio.sleep(0.01)
    
    # for i in range(num_pixels-1, 0-buffer, -1):
    #     if i<num_pixels and i>0:
    #         pixels[i] = pulse_color
    #     if i+buffer<num_pixels:
    #         pixels[i+buffer] = main_color
    #     pixels.show()
    #     await asyncio.sleep(0.01)


# while True:
#     switch.update()
    
#     if switch.pressed:
#         pulsating_light()
#         color_ind = (color_ind + 1) % (len(color_pairs)-1)
#         pixels.fill(color_pairs[color_ind][0])
#         pixels.show()

async def switch_handler():
    global color_ind
    while True:
        switch.update()

        if switch.pressed:
            color_ind = (color_ind + 1) % (len(color_pairs)-1)
            await asyncio.sleep(0.01)

async def main():
    pixels.fill(color_pairs[color_ind][0])
    pixels.show()
    pulsating_light_task = asyncio.create_task(pulsating_light())
    switch_handler_task = asyncio.create_task(switch_handler())
    await asyncio.gather(pulsating_light_task, switch_handler_task)

asyncio.run(main())
