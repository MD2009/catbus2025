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
# from driver import *
# from config import *
# from auto import *

# config
brain = Brain()
controller = Controller(PRIMARY)

belt1 = Motor(Ports.PORT18)
belt2 = Motor(Ports.PORT20)
pivot = Motor(Ports.PORT16)
table = Motor(Ports.PORT15)

RF = Motor(Ports.PORT13)
RB = Motor(Ports.PORT17)
LF = Motor(Ports.PORT12)
LB = Motor(Ports.PORT19)

# driver
switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_FB(spd):
    LF.spin(FORWARD, spd)
    LB.spin(FORWARD, spd)
    RF.spin(FORWARD, -spd)
    RB.spin(FORWARD, -spd)

def drive_LR(spd): # test to make sure it isnt inversed. pos should be right & neg should be left
    LF.spin(FORWARD, spd)
    LB.spin(FORWARD, -spd)
    RF.spin(FORWARD, spd)
    RB.spin(FORWARD, -spd)

def drive_rot(spd): #turn left -> all axis values neg, turn right -> all axis values pos
    LF.spin(FORWARD, spd)
    LB.spin(FORWARD, spd)
    RF.spin(FORWARD, spd)
    RB.spin(FORWARD, spd)

def belt(spd):
    belt1.spin(FORWARD, spd)
    belt2.spin(FORWARD, -spd)

def brake(type):
    LF.stop(type)
    LB.stop(type)
    RF.stop(type)
    RB.stop(type)

def drive_auto(d): #distance in inches
    wheel_circ = 10.2101761 #3.25" diameter wheel
    rev = 360*(d/wheel_circ)
    LF.spin_for(FORWARD, rev)
    LB.spin_for(FORWARD, rev)
    LF.spin_for(FORWARD, -rev)
    LB.spin_for(FORWARD, -rev)

def switch(n):
    global switch_cnt
    switch_cnt += 1
    if switch_cnt//2 == switch_cnt/2:
        coef = 1
    else:
        coef = -1
    # full rotation = 90, half = 60
    pivot.spin_to_position(60, DEGREES, False) #false = do not wait for completion
    table.spin_for(FORWARD, coef*252)
    if n == "dock":
        pivot.spin_to_position(90, DEGREES, False)
        pivot.reset_position()
    elif n == "end":
        pivot.spin_to_position(0, DEGREES, False)
    pivot.reset_position()
    # pivot.stop(HOLD)
    # do i need this

def manual_reset(): # lack of sensors :/
    # manually return to neutral position then activate
    controller.rumble('_')
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

# main
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # auto.sequence()
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
            controller.rumble('..')
        elif table.position() < -275:
            controller.rumble('..')

        # manual adjust
        if controller.buttonL1.pressing():
            pivot.spin(FORWARD, 10) # test to adjust rpm values
        elif controller.buttonR1.pressing():
            pivot.spin(FORWARD, -10)
        else:
            pivot.stop(HOLD)
        if controller.buttonL2.pressing():
            table.spin(FORWARD, 10)
        elif controller.buttonR2.pressing():
            table.spin(FORWARD, -10)
        else:
            table.stop(HOLD)

        ax1 = controller.axis1.position()
        ax2 = controller.axis2.position()
        ax3 = controller.axis3.position()
        ax4 = controller.axis4.position()
        # oh my god the joystick value can change during the time it takes for vs to
        # read the next line right under it thats nuts
        # maintain the joystick value w/ these variables to prevent divide by zero excp.

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