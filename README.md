# AltitudeLamp
## About
The AltitudeLamp is a resin project I built with an integrated WS2812 lightstrip (commonly known as NeoPixels) and a Raspberry Pi Pico W to control the lights. The Pico W spawns a WiFi hotspot with a web interface at the local address `192.168.4.1`.

## How To Use
Flash MicroPython firmware to the Pico W, and then upload all the files in this repo plus the NeoPixel driver (see `neopixel.py` below).
Here is a description of each file:

- `patterns.json` |Defines each light pattern by splitting it into frames, where each frame holds one RGB array per pixel. Also defined is the frame count, which must match the number of frames; and the rate, which is the framerate defined in seconds (or decimal variations thereupon).
- `neopixel.py` | The MicroPython driver for running the WS2812/NeoPixel lights, downloaded from the micropython-lib GitHub repo at https://github.com/micropython/micropython-lib/blob/d8e163bb5f3ef45e71e145c27bc4f207beaad70f/micropython/drivers/led/neopixel/neopixel.py
-
-
