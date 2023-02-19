import time
import max30100
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 17
LED_CURRENT_IR = 7.6

def button_pressed_callback(GPIO_pin_interrupted):
    print("Button pressed")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)    



mx30 = max30100.MAX30100(led_current_ir = LED_CURRENT_IR)
mx30.enable_spo2()

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup (BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Enable Interrupts
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_pressed_callback, bouncetime=200)

while 1:
    mx30.read_sensor()

    mx30.ir, mx30.red

    hb = int(mx30.ir / 100 )
    spo2 = int(mx30.red / 100)
    
    if mx30.ir != mx30.buffer_ir :
        print("Pulse:",hb)
    if mx30.red != mx30.buffer_red:
        print("SPO2:",spo2)
    
    time.sleep(1)