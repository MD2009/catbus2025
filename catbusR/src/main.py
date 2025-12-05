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

belt1 = Motor(Ports.PORT9)
belt2 = Motor(Ports.PORT10)
pivot = Motor(Ports.PORT8)
table = Motor(Ports.PORT7)

RF = Motor(Ports.PORT19)
RB = Motor(Ports.PORT6)
LF = Motor(Ports.PORT18)
LB = Motor(Ports.PORT5)

# driver
switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x))

def drive_FB(spd, type = RPM):
    LF.spin(FORWARD, -spd, type)
    LB.spin(FORWARD, -spd, type)
    RF.spin(FORWARD, spd, type)
    RB.spin(FORWARD, spd, type)

def drive_LR(spd, type = RPM): # test to make sure it isnt inversed. pos should be right & neg should be left
    LF.spin(FORWARD, -spd, type)
    LB.spin(FORWARD, spd, type)
    RF.spin(FORWARD, -spd, type)
    RB.spin(FORWARD, spd, type)

def drive_rot(spd, type = RPM): #turn left -> all axis values neg, turn right -> all axis values pos
    LF.spin(FORWARD, -spd, type)
    LB.spin(FORWARD, -spd, type)
    RF.spin(FORWARD, -spd, type)
    RB.spin(FORWARD, -spd, type)

def belt(spd):
    belt1.spin(FORWARD, spd)
    belt2.spin(FORWARD, -spd)

def brake(type):
    LF.stop(type)
    LB.stop(type)
    RF.stop(type)
    RB.stop(type)

def drive_auto(dir, dis, spd): # distance in inches
    if dir == "fb":
        drive_FB(spd)
    elif dir == "lr":
        drive_LR(spd)
    elif dir == "rt":
        drive_rot(spd)
    wait((dis/20)*(math.fabs(spd)/60), SECONDS) # 20" per rev, 1:1 green 4" wheel
    brake(BRAKE)
    wait(100, MSEC)

def spin_to_deg(motor, deg, spd, to = 5, tol = 5):
    dif = deg-motor.position()
    t = 0
    motor.spin_for(FORWARD, dif, DEGREES, spd, RPM, True)
    while math.fabs(dif) > tol and t < to:
        if motor.position() > deg:
            motor.spin_for(FORWARD, -dif*0.5, DEGREES, spd, RPM, False)
        elif motor.position() < deg:
            motor.spin_for(FORWARD, dif*0.5, DEGREES, spd, RPM, False)
        wait(50, MSEC)
        t+=0.05
        print(dif)
    motor.stop(BRAKE)
    print("finished")

def spin_to_rev(motor, rev, spd, to = 5, tol = 5):
    dif = rev-motor.position()
    t = 0
    motor.spin(FORWARD, spd)
    while math.fabs(dif) > tol and t < to:
        if motor.position() > rev:
            motor.spin(FORWARD, spd*-dif*0.5, RPM, False)
        elif motor.position() < rev:
            motor.spin(FORWARD, spd*dif*0.5, RPM, False)
        wait(50, MSEC)
        t+=0.05
    motor.stop(BRAKE)

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

def manual_reset(): # lack of sensors :/
    # manually return to neutral position then activate
    controller.rumble('_')
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

def autonomous():
    brain.screen.clear_screen()
    drive_auto("fb", 12, -75)
    belt(100)
    wait()
    belt1.stop(HOLD)
    belt2.stop(HOLD)
    drive_auto("fb", -2, 75)
    belt(100)   

def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

def user_control():
    brain.screen.clear_screen()
    pivot.set_timeout(2, SECONDS)
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
        if table.position() < -20:
            controller.rumble('__')
        elif table.position() > 275:
            controller.rumble('__')

        # manual adjust
        if controller.buttonL1.pressing():
            pivot.spin(FORWARD, 15)
            print(pivot.power())
        elif controller.buttonL2.pressing():
            pivot.spin(FORWARD, -15)
            print(pivot.power())
        else:
            pivot.stop(HOLD)
        if controller.buttonR1.pressing():
            table.spin(FORWARD, 15)
        elif controller.buttonR2.pressing():
            table.spin(FORWARD, -15)
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