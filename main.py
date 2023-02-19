import time
import max30100
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 17
BLUE_GPIO = 10 
GREEN_GPIO = 9 
RED_GPIO = 11
LED_HZ = 75
LED_CURRENT_IR = 7.6

# IRQ
def button_pressed_callback(GPIO_pin_interrupted):
    print("Button pressed")

# Take average BPM form FIFO buffer
def bpm_average(mx30):
    bpm_buffer = mx30.buffer_ir; 
    # Make sure buffer isn't null 
    if len(bpm_buffer)>0:
        sum = 0
        for i in range(0, len(bpm_buffer)):
            sum = sum + bpm_buffer[i] 
        return average = sum/len(bpm_buffer)
    return None


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

while 1:
    
    # Read the heart rate 
    mx30.read_sensor()
    mx30.ir
    hb = int(mx30.ir / 100 )
    if mx30.ir != mx30.buffer_ir :
        print("Pulse:", hb)
        bpm_avg = bpm_average(mx30)
        print("Average", bpm_avg)
    
    # Update led
    red.start(50/2.5)
    blue.start(100/2.5)
    green.start(1/2.5)
    
     
    time.sleep(1)