import blynklib

blynk = blynklib.Blynk("IwQyTY8WqD0SkkLROJM9mHomLPOrzRrj")

heartrate = "2k"


@blynk.handle_event("read V0")
def read_bpm(pin):
    blynk.virtual_write(pin, heartrate)
    print("written")


while True:
    blynk.run()
