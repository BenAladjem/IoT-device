
import time
from machine import Pin

led = Pin(14, Pin.OUT)
led_y = Pin(4, Pin.OUT)
led.on()
led_y.on()
relay1 = Pin(12, Pin.OUT)
relay2 = Pin(13, Pin.OUT)
relay1.value(1)
relay2.value(1)

def beep():
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)

def led_ligth():
    for i in range(3):
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)

for i in range(5):
    relay1.value(0)
    time.sleep(1)
    relay1.value(1)
    led_ligth()
    time.sleep(3)
    
'''
while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
'''


