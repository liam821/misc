#!/usr/bin/env python

import time

def rled(_inputtime=time.time()):

    '''
 
        Input epoch time (unixtime) and it will return a list of 64 leds, with a moving "blob" 5-6 wide
        that scrolls from one side to the other over 24 hours

    '''

    number_of_leds = 64
    # blob_size must be an odd number
    blob_size = 5
    led = [0] * number_of_leds

    lt = time.localtime(_inputtime)

    current_seconds = (lt[3]*60*60) + (lt[4]*60) + lt[5]
    wheremai_float = (current_seconds * float(number_of_leds-(blob_size-1))) / float(86400) + ((blob_size-1)/2)
    whereami_int = int(wheremai_float)

    print time.ctime(_inputtime)
    #print current_seconds
    #print wheremai_float
    #print whereami_int

    for i in range(whereami_int-((blob_size-1)/2)+1,whereami_int+((blob_size-1)/2)):
        led[i] = 1

    led[whereami_int-(blob_size/2)] = round(1-(wheremai_float % 1),2)
    led[whereami_int+(blob_size/2)] = round(wheremai_float % 1,2)

    return led

# 1 second before midnight
#print rled(1559631599)
# 1 second after midnight
#print rled(1559631599+2)
# current time
print rled()
