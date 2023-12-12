try:
    import usocket as socket        #importing socket
except:
    import socket
import network 
from machine import Pin
import time
import neopixel
import json
import _thread
import gc

with open('config.json', 'r') as configfile:
    config = json.load(configfile)

light_count = config["light_count"] # 10 lights on the reel
pin_num = config["pin"] # Pin 0
ssid = config["ap_ssid"]
password = config["ap_key"]

with open('patterns.json', 'r') as patternfile:
    patterns = json.load(patternfile)

with open('index.html', 'r') as webpagefile:
    html = webpagefile.read()

global np
np = neopixel.NeoPixel(Pin(pin_num), light_count)

# == ======= ==

# == Process ==
# Load index into variable
# Load light patterns into variable
# Load config options into variable

# Spin up AP
# Spin up web server
# When site changes, do an ASYNC call to change light pattern variable
#	Light pattern contents:
#	- Number of frames
#	- Framerate (s)
#	- Frames array
#	- Each frame is an array of 10 tuples, where each tuple is 3 values, RGB.
# Light process is a while loop that checks the active pattern name matches the current pattern, and contains a for loop that gets the relevant light pattern, reads the amount of frames, and loops that between 0 and n-1. Then loops through each light and sets.

continue_pattern = False

def update_pixels_in_frame(pattern, frame):
    for pixel in range(0, light_count):
        np[pixel] = patterns[pattern]["frames"][frame][pixel]
    np.write()
    time.sleep(float(patterns[pattern]["rate"]))
    
def run_pattern(pattern):
    if pattern == "off":
        np.fill((0, 0, 0))
        np.write()
    else:
        while continue_pattern == True:
            for frame in range(0, int(patterns[pattern]["frame_count"])):
                lock.acquire()
                update_pixels_in_frame(pattern, frame)
                lock.release()
                if continue_pattern == False:
                    return

def light_ctrl_thread(pattern):
    global continue_pattern
    continue_pattern = True
    run_pattern(pattern)

def kill_lights():
    global continue_pattern
    
    continue_pattern = False
    time.sleep(0.1)

def srvr_ctrl_thread():
    gc.collect()


    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)            #activating

    while ap.active() == False:
      pass
    print('Connection is successful')
    print(ap.ifconfig())
    def web_page():
      return html
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('192.168.4.1', 80))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Received HTTP GET connection request from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            print('GET Rquest Content = %s' % request)
            rainbow_active = request.find('/?rainbow')
            bw_active = request.find('/?bw')
            fadewhite_active = request.find('/?fadewhite')
            solidwhite_active = request.find('/?solidwhite')
            candyfloss_active = request.find('/?candyfloss')
            off_active = request.find('/?off')
            
            if rainbow_active == 6:
                print('RAINBOW ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("rainbow",))
                
                
            if bw_active == 6:
                print('BW ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("bw",))
                
            if fadewhite_active == 6:
                print('FADEWHITE ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("fadewhite",))
            
            if solidwhite_active == 6:
                print('SOLIDWHITE ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("solidwhite",))
                
            if candyfloss_active == 6:
                print('CANDYFLOSS ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("candyfloss",))
                
            if off_active == 6:
                print('OFF ACTIVE')
                kill_lights()
                active_light_thread = _thread.start_new_thread(light_ctrl_thread, ("off",))
                
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed')
    
    
    

lock = _thread.allocate_lock()
srvr_ctrl_thread()
