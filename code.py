import time
import board
import asyncio
import neopixel
import digitalio
from adafruit_debouncer import Button

pixel_pin = board.D1
num_pixels = 144
buffer = 30
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, brightness=0.6)
pin = digitalio.DigitalInOut(board.D2)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Button(pin)

color_pairs = [
    ((255, 0, 0), (100, 0, 0)),  # Red
    ((0, 255, 0), (0, 100, 0)),  # Green
    ((0, 0, 255), (0, 0, 100)),  # Blue
    ((255, 255, 0), (100, 100, 0)),  # Yellow
    ((0, 255, 255), (0, 100, 100)),  # Cyan
    ((255, 0, 255), (100, 0, 100))  # Magenta
]
color_ind = 0

async def pulsating_light():
    global color_pairs
    global color_ind
    global num_pixels
    global buffer
    while True:
        pulse_color, main_color = color_pairs[color_ind]
        for i in range(0, num_pixels+buffer):
            if i<num_pixels:
                pixels[i] = pulse_color
            pixels.show()
            if i>=buffer:
                pixels[i-buffer] = main_color
            pixels.show()
            await asyncio.sleep(0.01)

async def switch_handler():
    global color_ind
    while True:
        switch.update()
        if switch.pressed:
            pixels.fill(color_pairs[color_ind][1])
            color_ind = (color_ind + 1) % len(color_pairs)
            # pixels.fill(color_pairs[color_ind][0])
            # pixels.show()
        await asyncio.sleep(0.1)  


async def main():
    task1 = asyncio.create_task(pulsating_light())
    task2 = asyncio.create_task(switch_handler())
    await asyncio.gather(task1, task2)


asyncio.run(main())
