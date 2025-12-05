#!/bin/sh
# brightness
#x52cli bri led 44
#x52cli bri mfd 20

# on/off states
x52cli led fire on
x52cli led throttle on

# individual led colors
x52cli led a off
x52cli led b off
x52cli led e off
x52cli led d amber
x52cli led clutch off

# POV switch color
x52cli led pov off

# base levers color
x52cli led t1 off
x52cli led t2 amber
x52cli led t3 off

# blink of "i"(clutch) and POV
#x52cli blink off

# shift indicator on MFD
#x52cli shift off


