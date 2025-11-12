from vex import *
from config import *

switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_FB():
    LF.spin(FORWARD, curve(controller.axis3.position()))
    LB.spin(FORWARD, curve(controller.axis3.position()))
    RF.spin(FORWARD, curve(controller.axis3.position()))
    RB.spin(FORWARD, curve(controller.axis3.position()))
    wait(25, MSEC)

def drive_LR(): # test to make sure it isnt inversed. pos should be right & neg should be left
    LF.spin(FORWARD, curve(controller.axis4.position()))
    LB.spin(FORWARD, -curve(controller.axis4.position()))
    RF.spin(FORWARD, curve(controller.axis4.position()))
    RB.spin(FORWARD, -curve(controller.axis4.position()))
    wait(25, MSEC)

def drive_rot(): #turn left -> all axis values neg, turn right -> all axis values pos
    LF.spin(FORWARD, curve(controller.axis1.position()))
    LB.spin(FORWARD, curve(controller.axis1.position()))
    RF.spin(FORWARD, curve(controller.axis1.position()))
    RB.spin(FORWARD, curve(controller.axis1.position()))

def brake(type):
    LF.stop(type)
    LB.stop(type)
    RF.stop(type)
    RB.stop(type)

def all_brake():
    LF.stop(COAST)
    LB.stop(COAST)
    RF.stop(COAST)
    RB.stop(COAST)
    pivot.stop(HOLD)
    table.stop(HOLD)
    belt1.stop(HOLD)
    belt2.stop(HOLD)

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