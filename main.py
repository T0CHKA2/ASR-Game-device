import machine, os
from machine import Pin
from time import sleep

timer_red = machine.Timer(1)
timer_blue = machine.Timer(2)

flag_red = False
flag_blue = False

time_blue = 0
time_red = 0

led_red = Pin(15, Pin.OUT)
push_button_red = Pin(18, Pin.IN)

led_blue = Pin(13, Pin.OUT)
push_button_blue = Pin(12, Pin.IN)

def plustimered():
  global time_red
  time_red = time_red + 1

def plustimeblue():
  global time_blue
  time_blue = time_blue + 1

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
    timer_red.init(mode=machine.Timer.ONE_SHOT, period=1000, callback=plustimered())
  elif flag_blue:
      timer_blue.init(mode=machine.Timer.ONE_SHOT, period=1000, callback=plustimeblue())
  
  # Button interaction
  if logic_state_blue and logic_state_red:
    led_red.on()
    led_blue.on()
    flag_red = False
    flag_blue = False
    turnoff()
    sleep(10)
    print(1)
    f = open('timestamp.txt', 'a')
    f.write("Time red (s) = " + str(round(time_red/150)) + '\n' + "Time blue (s) = " + str(round(time_blue/150)))
    f.close()
    print(f.read())
    sleep(60)
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

  # Time report
  if flag_stop is True:
    pass
  elif flag_blue or flag_red:
    print("fast rep, red team = " + str(round(time_red/150)))
    print("fast rep, blue team = " + str(round(time_blue/150)))
