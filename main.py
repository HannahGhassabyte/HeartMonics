import time
import max30100
import signal
import sys
import RPi.GPIO as GPIO
from RPLCD import i2c
from time import sleep
import math
from spotify import *

BUTTON_GPIO = 17
BLUE_GPIO = 10 
GREEN_GPIO = 9 
RED_GPIO = 11
LED_HZ = 75
LED_CURRENT_IR = 7.6

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 16
i2c_expander = 'PCF8574'
address = 0x27
backlight = False 
lcd = i2c.CharLCD(i2c_expander, address, backlight)
lcd.cursor_pos = (0, 5)


# IRQ
def button_pressed_callback(GPIO_pin_interrupted):
    print("Button pressed")
    toggle_play(sp)

# Take average BPM form FIFO buffer
def bpm_average(mx30):
    bpm_buffer = mx30.buffer_ir; 
    # Make sure buffer isn't null 
    if len(bpm_buffer)>3:
        sum = 0
        for i in range(1, 5):
            sum = sum + bpm_buffer[-i] 
        return (sum/(400))
    return 0


# Intialze perpherials
mx30 = max30100.MAX30100(led_current_ir = LED_CURRENT_IR)
mx30.enable_spo2()

# button setup
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup (BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#rgb led setup 
GPIO.setup(BLUE_GPIO, GPIO.OUT)
GPIO.setup(GREEN_GPIO, GPIO.OUT)
GPIO.setup(RED_GPIO, GPIO.OUT)

# create objects from pwm 
blue = GPIO.PWM(BLUE_GPIO, LED_HZ)
green = GPIO.PWM(GREEN_GPIO, LED_HZ)
red = GPIO.PWM(RED_GPIO, LED_HZ)

# Enable Interrupts
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_pressed_callback, bouncetime=200)

# Spotify Initializations
sp, playlist_slow, playlist_med, playlist_fast = spotify_init()
prev_playlist_type = -1
# Write a string on first line and move to next line

while 1:
    # Read the heart rate 
    mx30.read_sensor()
    mx30.ir
    hb = int(mx30.ir / 100 )
    if mx30.ir != mx30.buffer_ir :
        print("Pulse:", hb)
        bpm_avg = bpm_average(mx30)
        print("Average", bpm_avg)
        song_name, prev_playlist_type = hr_logic(HR_VALUE=bpm_avg, sp=sp, prev_playlist_type=prev_playlist_type, 
                                                playlist_slow=playlist_slow, 
                                                playlist_med=playlist_med, 
                                                playlist_fast=playlist_fast)
        if bpm_avg > 50:
            lcd.cursor_pos = (0, 0)
            string_write = "Heart Rate:" + str(math.trunc(bpm_avg))
            lcd.write_string (string_write)
            lcd.cursor_pos = (1, 0)
            string_write = "Song:" + str(song_name)
            lcd.write_string (string_write)
        else:
            lcd.cursor_pos=(0,2)
            lcd.write_string("Heartmonics")
            lcd.cursor_pos = (1,4)
            lcd.write_string ("<3 <3 <3" )
    
        
    
    
    # Update led
    red.start(50/2.5)
    blue.start(100/2.5)
    green.start(1/2.5)
    
