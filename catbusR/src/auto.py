from vex import *
from driver import *

posY = 0.0
posX = 0.0

def auto_drive(dir, pos):
    
    if dir == "fb":
        global posY
        dif1 = pos-posY
        dif = dif1
        while dif > 0.1:
            drive_FB(dif/dif1) # percent of distance incompleted
            wait(10, MSEC)
            spd = 39.3700787*inert.acceleration(ZAXIS)*0.01 # convert to in
            posY += spd*0.01
            dif = pos-posY
    elif dir == "lr":
        global posX
        dif1 = pos-posX
        dif = dif1
        while dif > 0.1:
            drive_LR(dif/dif1)
            wait(10, MSEC)
            spd = 39.3700787*inert.acceleration(XAXIS)*0.01
            posX += spd*0.01
            dif = pos-posX
    elif dir == "rot":
        dif1 = pos-inert.heading()
        dif = dif1
        while dif > 0.1:
            drive_rot(dif/dif1)
            wait(10, MSEC)
            dif = pos-inert.heading()

def sequence():
