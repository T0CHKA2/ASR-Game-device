import os, ujson
from machine import Pin, Timer
from time import sleep

# Get needed data from settings.json
f_stngs = open("settings.json")
pin_data = ujson.load(f_stngs)

# Timer init
timer = Timer(0)

# Flag for some sort of chronometer timer
flag_red = False
flag_blue = False
time_blue = 0
time_red = 0

# Pins
led_red = Pin(pin_data["led_red"], Pin.OUT)
push_button_red = Pin(pin_data["button_red"], Pin.IN)

led_blue = Pin(pin_data["led_blue"], Pin.OUT)
push_button_blue = Pin(pin_data["button_blue"], Pin.IN)

# Timer custom callbacks
def plustimered():
  global time_red
  time_red = time_red + 1

def plustimeblue():
  global time_blue
  time_blue = time_blue + 1

# Turn off mechanics (fully)
def turnoff():
  flag_stop = True

flag_stop = False


while not flag_stop:
  logic_state_blue = push_button_blue.value()
  logic_state_red = push_button_red.value()
  led_state_red = led_red.value()
  led_state_blue = led_blue.value()

  # Timer data report
  if flag_red:
    timer.init(mode=Timer.ONE_SHOT, period=1000, callback=plustimered())
  elif flag_blue:
      timer.init(mode=Timer.ONE_SHOT, period=1000, callback=plustimeblue())
  
  # Button interaction
  if logic_state_blue and logic_state_red:
    led_red.on()
    led_blue.on()
    flag_red = False
    flag_blue = False
    turnoff()
    sleep(10) # Debug feature
    print(1) # Debug feature
    f = open('timestamp.txt', 'a')
    f.write("Time red (s) = " + str(round(time_red/150)) + '\n' + "Time blue (s) = " + str(round(time_blue/150)))
    f.close()
    print(f.read()) # Debug feature
    sleep(60) # Debug feature
  elif logic_state_red and not led_state_red:
    led_red.on()
    led_blue.off()
    
    flag_blue = False
    flag_red = True
  elif logic_state_blue and not led_state_blue:
    led_blue.on()
    led_red.off()
    
    flag_red = False
    flag_blue = True

  # Time report, yeah, this will spam
  if flag_stop is True:
    pass
  elif flag_blue or flag_red:
    print("fast rep, red team = " + str(round(time_red/150)))
    print("fast rep, blue team = " + str(round(time_blue/150)))
