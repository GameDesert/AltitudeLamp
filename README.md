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
### Setting Up Board and Lights
***WARNING: Please do not follow these instructions blindly. Make sure you always know exactly what you are doing and why you are doing it.***
***ANOTHER WARNING: Ensure your lightstrip's data arrows point away from your microcontroller and where you are soldering to. The data must travel away, not towards.***
***YET ANOTHER WARNING: Always stay safe when working around electricity or hot implements such as soldering irons. Children should, at best, not follow any of the steps described in this guide, and at least get the supervision of a responsible adult if they choose to do so anyway.***
1. Solder your lightstrip's ground to any of the Pico W's ground pins (these can be identified by the square-ended, sharp cornered copper traces, but always double check a pinout guide).
2. Solder your lightstrip's data wire to GPIO pin 0 (usually labelled *1* on the board, but again, always consult a pinout guide), or any other suitable GPIO pin.
3. Finally, solder your lightstrip's power line to the 3.3V pin on the Pico (not the 5V, and definitely not 3V3_EN. Once more, **always consult a pinout guide!!**). This is because WS2812 lights have a certain tolerance where the data pin must be somewhere around 70% of the power pin's voltage *at a minimum*, a requirement not satisfied when the lights are connected to the Pico W's 5V output which can lead to weirdly coloured, damaged, or malfunctioning lights.

![Circuit diagram for Raspberry Pi Pico W and WS2812 lightstrip](https://kotla.eu/files/altitude_board_diagram.svg)

### Adding Light Patterns
1. Define a new pattern in the patterns.json file, specifying the name of the pattern (as the dictionary key), the number of frames, the framerate in seconds, and the frames themselves (with RGB values for each pixel). Ensure there are only as many pixel colour definitions as there are pixels attached to your Pico W (or similar board, but this project really is intended for the Pico W) and as defined in the `light_count` attribute in the `config.json` file. Also, the real number of frames should match the number you declare under the `frame_count` variable in `patterns.json`.
2. In `main.py`, there is a function called `srvr_ctrl_thread`. Inside that function is a while loop. Inside that while loop is a try/except statement. In the try portion of the try/except statement are 2 important groups of lines, the first taking the shape `[pattern]_active = request.find('/?[abbreviation]')`. To add a pattern, create a new line like this right underneath replacing `[pattern]` in the variable name with a memorable name for your pattern, it doesn't really matter what it is as long as it doesn't conflict with any other variable names. Then, replace `[abbreviation]` with the name or abbreviation you wish to represent your pattern in the interface URL when the user clicks on the corresponding button (see step 4).
3. Only a few lines later you will find some if statements beginning `if [pattern]_active == 6:`. Copy all 4 lines and replace `[pattern]` with the memorable name you chose in step 2. The print statement in the second line is redundant, as there is no visible console output when running this entire setup, but I left it in for debugging and you can set the statement to say anything you want. The key line is the one after `kill_lights()` (very important, do not delete), which looks like this: `active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("[pattern.json reference]",))`. Replace `[pattern.json reference]` with whatever you named your pattern in `pattern.json`.
4. Finally, add your pattern's button to the interface in the `index.html` file. This can be done by adding two lines above the link for **"LIGHTS OFF"**. The first line should be a line break (`<br>`), and the second line should be an anchor link to the URL (specifically, the query flag) you set in step 2. The format is as follows: `<a href="/?[abbreviation]" title="[descriptive text]" target="_self">[fancy emoji]</a>` where `[abbreviation]` is the abbreviation for the URL, `[descriptive text]` is a quick phrase to describe your pattern (like its name), and `[fancy emoji]` is a few colourful emoji squares to represent the general vibe of what your pattern looks like.
5. Just like that, you've added a new pattern! See below to find out how to configure the access point and deploy the Pico W.

### Configuration and Deployment
1. In `config.json`, replace the values for `[access point name]` and `[access point password]` with you preferred values for the name and password to the WiFi access point, respectively. These should probably be simple strings; I haven't tested it but WiFi SSIDs tend to be quite fragile things when it comes to emoji and stuff.
2. Make sure the value for `pin` matches the GPIO pin to which your lightstrip's data lead is soldered, by default pin 0 here (well, called pin 0 but labelled *1* on the board).
3. Make sure the value for `light_count` accurately describes the precise number of lights there are on your strip, or funny things might happen (not haha funny, more ohnomylightshavestoppedworkingandidon'tknowwhy funny).
4. Finally, save everything and plug your Pico W into an appropriate power source (see manufacturer's instructions) to test it out. You should see a new WiFi network appear on any nearby mobile devices that, when connected, will let you navigate to the IP address `192.168.4.1` to access the interface (I've tried changing this address, I don't know how to, so it's just that unwieldy set of random numbers). *Please note: This WiFi network does not have access to the internet. It's not a portable hotspot.*
