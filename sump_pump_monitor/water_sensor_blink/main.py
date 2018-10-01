"""
    Script to blink an LED connected to GPIO Pin 2 of the ESP 8266 board
    based on the presence or lack thereof of water provided on GPIO Pin 0
    using an Optimax Digital Liquid Level Sensor.
"""

###########################################################################
# Setup code goes below, this is called once at the start of the program: #
###########################################################################
import machine
import time

led = machine.Pin(4, machine.Pin.OUT)

# Counter 
sensor = machine.Pin(14, machine.Pin.IN)

while True:
    ###################################################################
    # Loop code goes inside the loop here, this is called repeatedly: #
    ###################################################################
    if(sensor.value() == 0):
        led.on()
    else:
        led.off()
    time.sleep(2.0)  # Delay for 2 seconds.


