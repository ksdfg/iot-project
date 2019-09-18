import time

# Import the ADS1x15 module.
import adafruit_ads1x15.ads1115 as ads
import adafruit_ads1x15.analog_in as analog_in
import board
import busio

adc = ads.ADS1115(busio.I2C(board.SCL, board.SDA))

# initialization 
GAIN = 2 / 3
curState = 0
thresh = 525  # mid point in the waveform
P = 512
T = 512
stateChanged = 0
sampleCounter = 0
lastBeatTime = 0
firstBeat = True
secondBeat = False
Pulse = False
IBI = 600
rate = [0] * 10
amp = 100

lastTime = int(time.time() * 1000)


# Main loop. use Ctrl-c to stop the code
def measure(func):
    # var list reqd.
    global GAIN
    global curState
    global thresh
    global P
    global T
    global stateChanged
    global sampleCounter
    global lastBeatTime
    global firstBeat
    global secondBeat
    global Pulse
    global IBI
    global rate
    global amp
    global lastTime

    # read from the ADC
    signal = analog_in.AnalogIn(adc, ads.P0).value  # get input from channel a0
    curtime = int(time.time() * 1000)

    sampleCounter += curtime - lastTime  # # keep track of the time in mS with this variable
    lastTime = curtime
    n = sampleCounter - lastBeatTime  # # monitor the time since the last beat to avoid noise

    # find the peak and trough of the pulse wave
    if signal < thresh and n > (IBI / 5.0) * 3.0:  # # avoid dichrotic noise by waiting 3/5 of last IBI
        if signal < T:  # T is the trough
            T = signal  # keep track of lowest point in pulse wave 

    if signal > thresh and signal > P:  # thresh condition helps avoid noise
        P = signal  # P is the peak
        # keep track of highest point in pulse wave

    #  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
    # signal surges up in value every time there is a pulse
    if n > 250:  # avoid high frequency noise
        if (signal > thresh) and not Pulse and (n > (IBI / 5.0) * 3.0):
            Pulse = True  # set the Pulse flag when we think there is a pulse
            IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
            lastBeatTime = sampleCounter  # keep track of time for next pulse

            if secondBeat:  # if this is the second beat, if secondBeat == TRUE
                secondBeat = False  # clear secondBeat flag
                for i in range(0, 10):  # seed the running total to get a realisitic bpm at startup
                    rate[i] = IBI

            if firstBeat:  # if it's the first time we found a beat, if firstBeat == TRUE
                firstBeat = False  # clear firstBeat flag
                secondBeat = True  # set the second beat flag
                return  # IBI value is unreliable so discard it

            # keep a running total of the last 10 IBI values
            running_total = 0  # clear the running_total variable    

            for i in range(0, 9):  # shift data in the rate array
                rate[i] = rate[i + 1]  # and drop the oldest IBI value 
                running_total += rate[i]  # add up the 9 oldest IBI values

            rate[9] = IBI  # add the latest IBI to the rate array
            running_total += rate[9]  # add the latest IBI to running_total
            running_total /= 10  # average the last 10 IBI values 
            bpm = 60000 / running_total  # how many beats can fit into a minute? that's bpm!
            func('bpm: {}'.format(bpm))

    if signal < thresh and Pulse:  # when the values are going down, the beat is over
        Pulse = False  # reset the Pulse flag so we can do it again
        amp = P - T  # get amplitude of the pulse wave
        thresh = amp / 2 + T  # set thresh at 50% of the amplitude
        P = thresh  # reset these for next time
        T = thresh


if __name__ == '__main__':
    while True:
        measure(print)
        time.sleep(0.005)
