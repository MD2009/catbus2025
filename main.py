# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       morga                                                        #
# 	Created:      11/12/2025, 9:09:29 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from config import *
from driver import *
import auto

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    auto.sequence()
    # place automonous code here

def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    device_check()
    # place driver control in this while loop
    while True:
        if controller.buttonX.pressing():
            switch()
        if abs(controller.axis3.position()) < 1 and abs(controller.axis2.position()) < 1:
            brake(COAST)
        else:
            drive_con()
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()