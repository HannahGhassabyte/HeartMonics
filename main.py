import time
import max30100

mx30 = max30100.MAX30100(led_current_ir=7.6)
mx30.enable_spo2()

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup (17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while 1:
    mx30.read_sensor()

    mx30.ir, mx30.red

    hb = int(mx30.ir / 100 )
    spo2 = int(mx30.red / 100)
    
    if mx30.ir != mx30.buffer_ir :
        print("Pulse:",hb)
    if mx30.red != mx30.buffer_red:
        print("SPO2:",spo2)