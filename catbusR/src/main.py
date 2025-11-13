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
        # action hotkeys
        if controller.buttonX.pressing():
            switch("dock")
        if controller.buttonA.pressing():
            switch("end")

        # control
        if controller.buttonUp.pressing():
            manual_reset()
        if table.position() > 20:
            controller.rumble('..')
            while table.position() > 20: # def needs testing i doubt itll be this accurate
                table.spin(FORWARD, -20)
            table.stop(HOLD)
        elif table.position() < -275:
            controller.rumble('..')
            while table.position() < -275:
                table.spin(FORWARD, 20)
            table.stop(HOLD)

        # manual adjust
        if controller.buttonL1.pressing():
            pivot.spin(FORWARD, 25) # test to adjust rpm values
        elif controller.buttonR1.pressing():
            pivot.spin(FORWARD, -25)
        else:
            pivot.stop(HOLD)
        if controller.buttonL2.pressing():
            table.spin(FORWARD, 25)
        elif controller.buttonR2.pressing():
            table.spin(FORWARD, -25)
        else:
            table.stop(HOLD)
        
        if abs(controller.axis2.position()) > 1:
            belt()
        else:
            belt1.stop(HOLD)
            belt2.stop(HOLD)

        if abs(controller.axis3.position()) > 1 or abs(controller.axis1.position()) > 1 or abs(controller.axis4.position()) > 1:
            drive_FB()
            drive_LR()
            drive_rot()
        else:
            brake(COAST)
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()