print("RUN: boot.py")


'''
from machine import Pin
import time

p2 = Pin(2, Pin.IN)
p4 = Pin(4, Pin.IN)
p14 = Pin(14, Pin.OUT)

p14.value(1)
'''
#b = 70
#tim = b // 100
#h = tim // 3600
#m = (tim % 3600)//60
#sec = tim % 60
#milisec = b % 100
'''
tim = 0
timer = 0
p2.value(1)
sto = 0
sta = 0

def print_time(timer):
    tim = timer // 100
    h = tim // 3600
    m = (tim % 3600)//60
    sec = tim % 60
    milisec = timer % 100
    print(h,':',m,':',sec,':',milisec)
    
def start(n):
    p2.irq(handler = None)
    print('Start')
    if p14.value() == 1:
        p14.value(0)
        
    time.sleep(1)
    #p4.irq(handler = stop,  trigger= Pin.IRQ_FALLING | Pin.IRQ_RISING)
    p2.irq(handler=start, trigger= Pin.IRQ_FALLING | Pin.IRQ_RISING)
    

def stop(sta):
    p4.irq(handler = None)
    print('Stop')
    if p14.value() == 0:
        p14.value(1)
    
    time.sleep(1)    
    p4.irq(handler = stop, trigger = Pin.IRQ_FALLING| Pin.IRQ_RISING)
    
    
p2.irq(handler = start, trigger= Pin.IRQ_FALLING | Pin.IRQ_RISING)
p4.irq(handler = stop,  trigger= Pin.IRQ_FALLING | Pin.IRQ_RISING)

'''





