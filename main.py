from threading import Thread

import blynklib

blynk = blynklib.Blynk("IwQyTY8WqD0SkkLROJM9mHomLPOrzRrj")

measuring = False


@blynk.handle_event("write v1")
def change_state(pin, value):
    print(pin, value)
    global measuring
    measuring = value[0] == '1'


def measure():
    while True:
        if measuring:
            '''
            measure pulse rate here
            '''
            print("measuring")


Thread(target=measure).start()
while True:
    blynk.run()
