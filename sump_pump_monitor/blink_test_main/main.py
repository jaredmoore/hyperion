"""
    Script to blink an LED connected to GPIO Pin 2 of the ESP 8266 board.
"""

###########################################################################
# Setup code goes below, this is called once at the start of the program: #
###########################################################################
import machine
import time

# Counter 
i = 1
led = machine.Pin(4, machine.Pin.OUT)

while True:
    ###################################################################
    # Loop code goes inside the loop here, this is called repeatedly: #
    ###################################################################
    i += 1
    i = i % 2
    if(i % 2 == 0):
        led.on()
    else:
        led.off()
    time.sleep(2.0)  # Delay for 2 seconds.

