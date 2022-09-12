# Smart Cutebot + Pico:ed by Elecfreaks - My Line Follower example 
# by @Cyb3rn0id on Hackster.io
# https://www.hackster.io/CyB3rn0id/getting-started-with-the-pico-ed-smart-cutebot-a33334

from cutebot import * # import all functions from cutebot library
import time
from picoed import * # import all functions from picoed library (frozen module)

# Create an instance of cutebot object
cutebot = Cutebot()    

# At start we will show an image on the dotmatrix display
# some images are embedded => see on:
# https://www.elecfreaks.com/learn-en/pico-ed/led-dot-matrix-screen.html
display.show(Image.EXCITED) 

# We will use this flag for start/stop the line following mode
started=False

# waiting for button A press to start the first time
while not button_a.is_pressed():
    time.sleep(0.01)

started=True

# Function for flashingof the 2 big leds on front
def Ready():
    # clear the dot matrix display
    display.clear()
    
    # more about music function, here => https://www.elecfreaks.com/learn-en/pico-ed/music.html
    music.set_tempo(4,200) #4 ticks, 200bpm
    i=0
    while i<=3:
        cutebot.set_light(RGB.left, 255, 255, 255) # white
        cutebot.set_light(RGB.right, 0, 0, 255) # blue
        music.play('c4')
        cutebot.set_light(RGB.left, 0, 0, 255) # blue
        cutebot.set_light(RGB.right, 255, 255, 255) # blue
        music.play('g')
        i+=1
    cutebot.set_light(RGB.left, 0, 255, 0) # green
    cutebot.set_light(RGB.right, 0, 255, 0) # green

search=False # flag used when robot is out of track, for searching it
# Function for make robot moving the line
# While true, detect the status of the line-tracking sensors
# In front of Cutebot there are 2 blue leds where tracking sensors are located
# a led is ON when the sensor detect a black (or non-reflecting) surface
# a led is OFF when there is a reflecting surface
def Run():
    
    # say mr.python I want to use these global defined variables here
    global search
        
    # the cutebot get_tracking() method returns a string that reflects the blue led statuses
    # more here => http://www.elecfreaks.com/learn-en/pico-ed-kit/pico-ed-cutebot-kit/the-line-following-car.html
    trace=cutebot.get_tracking()
    
    # both blue leds are on => black line under both sensors => go straight
    if trace=="11": 
        cutebot.set_speed(20,20)
        search=False
        display.show(Image.HAPPY)
        cutebot.set_light(RGB.left, 0, 255, 0) 
        cutebot.set_light(RGB.right, 0, 255, 0)
            
    # left blue led off, right blue led on => must turn to right rising left wheel speed
    elif trace=="01":
        cutebot.set_speed(20,5)
        search=False
        display.show(Image.PEEK_LEFT)
        cutebot.set_light(RGB.left, 0, 255, 0) 
        cutebot.set_light(RGB.right, 0, 255, 0)
    
    # left blue led on, right blue led off => must turn to left rising right wheel speed
    elif trace=="10":
        cutebot.set_speed(5,20)
        search=False
        display.show(Image.PEEK_RIGHT)
        cutebot.set_light(RGB.left, 0, 255, 0) 
        cutebot.set_light(RGB.right, 0, 255, 0)
     
    # both blue leds off => robot out of the line, stop and try to recover the line
    elif trace=="00":
        if search==False: # first time we're here after last out-of-the-track event
            Stop()
            search=True # set this flag so we'll not repeat those operations above
        
        cutebot.set_speed(-15,15) # move left
            
    else:
        pass

# Function for making robot stop
def Stop():
    cutebot.set_speed(0,0)
    display.show(Image.SUPERCILIOUS_LOOK)
    cutebot.set_light(RGB.left, 255, 0, 0) # red
    cutebot.set_light(RGB.right, 255, 0, 0) # red
    time.sleep(0.2) # stop 200ms
            
# main cycle, repeated forever
# robot will be started pressing A button
# and stopped pressing B button
while True:
    
    # Button B pressed => reset 'started' flag and stop the robot
    if button_b.is_pressed():
        started=False
        Stop()
        music.set_tempo(4,440)
        music.play(['f4','e4','d4','c4'])
    
    # Button A pressed => make start animation (Ready()) and set 'started' flag
    if button_a.is_pressed():
        Ready()
        started=True
    
    # flag started is true => call the Run() procedure
    # for make robot follow the line
    if started:
        Run()
