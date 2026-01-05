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
from driver import *
from config import *
from auto import *

def manual_reset(): # lack of sensors :/
    # manually return to neutral position then activate
    controller.rumble('_')
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

def autonomous():
    brain.screen.clear_screen()

    pivot.spin_to_position(-45, DEGREES, 30, RPM, True)
    belt(100)
    wait(2, SECONDS)
    belt1.stop(HOLD)
    belt2.stop(HOLD)

def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

def user_control():
    brain.screen.clear_screen()
    pivot.set_timeout(2, SECONDS)
    inert.calibrate()
    device_check()
    ax1 = 0
    ax2 = 0
    ax3 = 0
    ax4 = 0
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
            controller.rumble('.')
            print(table.position())
        elif table.position() < -275:
            controller.rumble('.')
            print(table.position())

        # manual adjust
        if controller.buttonL1.pressing():
            pivot.spin(FORWARD, 15)
        elif controller.buttonL2.pressing():
            pivot.spin(FORWARD, -15)
        else:
            pivot.stop(HOLD)
        if controller.buttonR1.pressing():
            table.spin(FORWARD, 25)
        elif controller.buttonR2.pressing():
            table.spin(FORWARD, -25)
        else:
            table.stop(HOLD)

        ax1 = controller.axis1.position()
        ax2 = controller.axis2.position()
        ax3 = controller.axis3.position()
        ax4 = controller.axis4.position()

        if abs(ax2) > 1:
            belt(ax2)
        else:
            belt1.stop(HOLD)
            belt2.stop(HOLD)

        if abs(ax3) > 1:
            drive_FB(ax3)
        elif abs(ax4) > 1:
            drive_LR(ax4)
        elif abs(ax1) > 1:
            drive_rot(ax1)
        else:
            brake(BRAKE)
        wait(20, MSEC)


# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()