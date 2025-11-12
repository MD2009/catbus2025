from vex import *
from config import *

switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_con():
    LF.spin(FORWARD, curve(controller.axis3.position()))
    LB.spin(FORWARD, curve(controller.axis3.position()))
    LF.spin(FORWARD, -curve(controller.axis3.position()))
    LB.spin(FORWARD, -curve(controller.axis3.position()))
    wait(25, MSEC)

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

def switch():
    global switch_cnt
    switch_cnt += 1
    # full rotation = 90, half = 60
    pivot.spin_to_position(60, DEGREES, False) #false = do not wait for completion
    if switch_cnt//2 == switch_cnt/2:
        table.spin_for(FORWARD, 252)
    else:
        table.spin_for(FORWARD, -252)