#!/bin/sh
# brightness
#x52cli bri led 44
#x52cli bri mfd 20

# on/off states
x52cli led fire on
x52cli led throttle on

# individual led colors
x52cli led a red
x52cli led b green
x52cli led e green
x52cli led d amber
x52cli led clutch red

# POV switch color
x52cli led pov amber

# base levers color
x52cli led t1 green
x52cli led t2 amber
x52cli led t3 red

# blink of "i"(clutch) and POV
#x52cli blink off

# shift indicator on MFD
#x52cli shift off


