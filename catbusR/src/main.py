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

belt1 = Motor(Ports.PORT13)
belt2 = Motor(Ports.PORT14)
pivot = Motor(Ports.PORT15)
table = Motor(Ports.PORT18)

RF = Motor(Ports.PORT19)
RB = Motor(Ports.PORT12)
LF = Motor(Ports.PORT20)
LB = Motor(Ports.PORT11)

# driver
switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_FB(spd):
    LF.spin(FORWARD, curve(spd))
    LB.spin(FORWARD, curve(spd))
    RF.spin(FORWARD, -curve(spd))
    RB.spin(FORWARD, -curve(spd))
    wait(25, MSEC)

def drive_LR(spd): # test to make sure it isnt inversed. pos should be right & neg should be left
    LF.spin(FORWARD, curve(spd))
    LB.spin(FORWARD, -curve(spd))
    RF.spin(FORWARD, curve(spd))
    RB.spin(FORWARD, -curve(spd))
    wait(25, MSEC)

def drive_rot(): #turn left -> all axis values neg, turn right -> all axis values pos
    LF.spin(FORWARD, curve(controller.axis1.position()))
    LB.spin(FORWARD, curve(controller.axis1.position()))
    RF.spin(FORWARD, curve(controller.axis1.position()))
    RB.spin(FORWARD, curve(controller.axis1.position()))

def belt():
    belt1.spin(FORWARD, curve(controller.axis2.position()))
    belt2.spin(FORWARD, -curve(controller.axis2.position()))

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

        ax1 = abs(controller.axis1.position())
        ax2 = abs(controller.axis2.position())
        ax3 = abs(controller.axis3.position())
        ax4 = abs(controller.axis4.position())
        # oh my god the joystick value can change during the time it takes for vs to
        # read the next line right under it thats nuts
        # maintain the joystick value w/ these variables to prevent divide by zero excp.

        if abs(controller.axis2.position()) > 1:
            belt()
        else:
            belt1.stop(HOLD)
            belt2.stop(HOLD)

        if ax3 > 1:
            drive_FB(ax3)
            print(ax3)
        if ax4 > 1:
            drive_LR(ax4)
            print(ax4)
        if ax1 > 1:
            drive_rot()
        else:
            brake(COAST)
        wait(20, MSEC)


# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()