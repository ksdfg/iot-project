from threading import Thread
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import blynklib


import pulse_rate as pr

blynk = blynklib.Blynk("IwQyTY8WqD0SkkLROJM9mHomLPOrzRrj")

measuring = False  # boolean to figure out if we are measuring right now or not

# when the user clicks button
@blynk.handle_event("write v1")
def change_state(pin, value):
    print(pin, value)
    global measuring
    measuring = value[0] == '1'
    

# measuring the pulse rate
def measure():
    while True:
        if measuring:  # measure pulse rate here
            pr.lastTime = int(time() * 1000)  # set to current time
            #pr.adc.start_adc()
            pr.measure(lambda x: blynk.virtual_write(0, x))  # measure pulse and send to app
            sleep(0.005)


Thread(target=measure).start()  # start measuring in seperate thread

while True:
    blynk.run()  # start polling for action from RPi
