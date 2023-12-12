# AltitudeLamp
## About
The AltitudeLamp is a resin project I built with an integrated WS2812 lightstrip (commonly known as NeoPixels) and a Raspberry Pi Pico W to control the lights. The Pico W spawns a WiFi hotspot with a web interface at the local address `192.168.4.1`.

## How To Install
Flash MicroPython firmware to the Pico W, and then upload all the files in this repo plus the NeoPixel driver (see `neopixel.py` below).
Here is a description of each file:

- `patterns.json` |Defines each light pattern by splitting it into frames, where each frame holds one RGB array per pixel. Also defined is the frame count, which must match the number of frames; and the rate, which is the framerate defined in seconds (or decimal variations thereupon).
- `neopixel.py` | The MicroPython driver for running the WS2812/NeoPixel lights, downloaded from the micropython-lib GitHub repo at https://github.com/micropython/micropython-lib/blob/d8e163bb5f3ef45e71e145c27bc4f207beaad70f/micropython/drivers/led/neopixel/neopixel.py
-
-

## How To Configure
### Adding Light Patterns
1. Define a new pattern in the patterns.json file, specifying the name of the pattern (as the dictionary key), the number of frames, the framerate in seconds, and the frames themselves (with RGB values for each pixel). Ensure there are only as many pixel colour definitions as there are pixels attached to your Pico W (or similar board, but this project really is intended for the Pico W) and as defined in the `light_count` attribute in the `config.json` file. Also, the real number of frames should match the number you declare under the `frame_count` variable in `patterns.json`.
2. In `main.py`, there is a function called `srvr_ctrl_thread`. Inside that function is a while loop. Inside that while loop is a try/except statement. In the try portion of the try/except statement are 2 important groups of lines, the first taking the pattern `[pattern]_active = request.find('/?[abbreviation]')`. To add a pattern, create a new line like this right underneath replacing `[pattern]` in the variable name with a memorable name for your pattern, it doesn't really matter what it is as long as it doesn't conflict with any other variable names. Then, replace `[abbreviation]` with the name or abbreviation you wish to represent your pattern in the interface URL when the user clicks on the corresponding button (see step 4).
3. Only a few lines later you will find some if statements beginning `if [pattern]_active == 6:`. Copy all 4 lines and replace `[pattern]` with the memorable name you chose in step 2. The print statement in the second line is redundant, as there is no visible console output when running this entire setup, but I left it in for debugging and you can set the statement to say anything you want. The key line is the one after `kill_lights()` (very important, do not delete), which looks like this: `active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("[pattern.json reference]",))`. Replace `[pattern.json reference]` with whatever you named your pattern in `pattern.json`.
4. Finally, add your pattern's button to the interface in the `index.html` file.
