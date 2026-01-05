from vex import *
from config import *

switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_FB(spd, type = RPM):
    LF.spin(FORWARD, curve(spd), type)
    LB.spin(FORWARD, curve(spd), type)
    RF.spin(FORWARD, curve(-spd), type)
    RB.spin(FORWARD, curve(-spd), type)

def drive_LR(spd, type = RPM): # test to make sure it isnt inversed. pos should be right & neg should be left
    LF.spin(FORWARD, curve(spd), type)
    LB.spin(FORWARD, curve(-spd), type)
    RF.spin(FORWARD, curve(spd), type)
    RB.spin(FORWARD, curve(-spd), type)

def drive_rot(spd, type = RPM): #turn left -> all axis values neg, turn right -> all axis values pos
    LF.spin(FORWARD, curve(spd), type)
    LB.spin(FORWARD, curve(spd), type)
    RF.spin(FORWARD, curve(spd), type)
    RB.spin(FORWARD, curve(spd), type)

def belt(spd):
    belt1.spin(FORWARD, spd)
    belt2.spin(FORWARD, -spd)

def belt_brake():
    belt1.stop()
    belt2.stop()

def brake(type):
    LF.stop(type)
    LB.stop(type)
    RF.stop(type)
    RB.stop(type)

def switch(n):
    global switch_cnt
    switch_cnt += 1
    if switch_cnt//2 == switch_cnt/2:
        coef = 1
    else:
        coef = -1
    # full rotation = 180, half = 90, a lot more accurate now w/ high srth axle & motor
    pivot.spin_to_position(-90, DEGREES, 40, RPM, True) #false = do not wait for completion
    # spin_to(pivot, -90) #starting pos must be w brain on right side & pivot motor on right side
    table.spin_to_position(coef*240, DEGREES, 50, RPM, True) #has to be a bit higher RPM than others
    if n == "dock":
        if coef == 1:
            pivot.spin_to_position(0, DEGREES, 40, RPM, True) # spin to position doesnt time out ._.
            # spin_to(pivot, 0)
        else:
            pivot.spin_to_position(-180, DEGREES, 40, RPM, True)
            # spin_to(pivot, -180) 
    elif n == "end":
        if coef == 1:
            pivot.spin_to_position(-180, DEGREES, 40, RPM, True)
            # spin_to(pivot, -180)
        else:
            pivot.spin_to_position(0, DEGREES, 40, RPM, True)
            # spin_to(pivot, 0)
    table.reset_position()
    # pivot.stop(HOLD)
    # do i need this

# def spin_to_deg(motor, deg, spd, to = 5, tol = 5):
#     dif = deg-motor.position()
#     t = 0
#     motor.spin_for(dif, spd, True)
#     while math.fabs(dif) > tol and t < to:
#         if motor.position() > deg:
#             motor.spin_for(-dif*0.5, DEGREES, spd)
#         elif motor.position() < deg:
#             motor.spin_for(dif*0.5, DEGREES, spd)
#         wait(50, MSEC)
#         t+=0.05
#     motor.stop(BRAKE)

# def spin_to_rev(motor, rev, spd, to = 5, tol = 5):
    # dif = rev-motor.position()
    # t = 0
    # motor.spin(FORWARD, spd)
    # while math.fabs(dif) > tol and t < to:
    #     if motor.position() > rev:
    #         motor.spin(FORWARD, spd*-dif*0.5, RPM, False)
    #     elif motor.position() < rev:
    #         motor.spin(FORWARD, spd*dif*0.5, RPM, False)
    #     wait(50, MSEC)
    #     t+=0.05
    # motor.stop(BRAKE)

def manual_reset():
    # manually return to neutral position then activate
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()