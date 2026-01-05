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

def autonomous():
    auto_drive("lr", -6)
    belt(70)
    auto_drive("fb", 48)
    wait(750, MSEC) # wait for block collection?
    belt_brake()

    auto_drive("rot", 45)
    pivot.spin_to_position(90, 40) #try spin_to_deg?
    auto_drive("fb", 84)
    belt(-70)
    wait(1500, MSEC) #score 2?
    belt_brake()
    pivot.spin_to_position(0, 40)
    auto_drive("fb", 48)

    auto_drive("rot", 0)
    auto_drive("lr", 54)
    auto_drive("rot", 315)
    auto_drive("fb", 84)
    belt(-70)
    wait(1500, MSEC) #score 2?
    belt_brake()
    auto_drive("fb", 48)

    auto_drive("rot", 0)
    auto_drive("fb", 36)
    auto_drive("lr", -102)
    pivot.spin_to_position(180)
    auto_drive("fb", 12)
    belt(-70)
    wait(2, SECONDS)
    belt_brake()

    auto_drive("fb", 42)
    belt(-70) #iunno just let it run until autons over?

def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

def user_control():
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
            belt_brake()

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