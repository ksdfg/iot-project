from time import sleep, time

import blynklib

blynk = blynklib.Blynk("IwQyTY8WqD0SkkLROJM9mHomLPOrzRrj")

heartrate = "2k"


@blynk.handle_event("write v1")
def change_state(pin, value):
    print(pin, value)
    if value[0] == '1':
        for i in range(60):
            blynk.virtual_write(0, i)
            sleep(1)


while True:
    blynk.run()
