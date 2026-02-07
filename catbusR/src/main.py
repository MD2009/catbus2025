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

# config
brain = Brain()
controller = Controller(PRIMARY)

belt1 = Motor(Ports.PORT13)
belt2 = Motor(Ports.PORT14)
pivot = Motor(Ports.PORT15)
table = Motor(Ports.PORT16)

RF = Motor(Ports.PORT19)
RB = Motor(Ports.PORT12)
LF = Motor(Ports.PORT18)
LB = Motor(Ports.PORT17)

inert = Inertial(Ports.PORT20)
dock1 = Bumper(Ports.PORT)
dock2 = Bumper(Ports.PORT)

# driver
switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x)) * 0.25

def drive(Rspd, Lspd, type):
    LF.spin(FORWARD, Lspd, type)
    LB.spin(FORWARD, -Lspd, type)
    RF.spin(FORWARD, Rspd, type)
    RB.spin(FORWARD, -Rspd, type)

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
    # full rotation = 180, half = 90, a lot more accurate now w/ high srth axle & motor
    pivot.spin_to_position(-90, DEGREES, 40, RPM)
    # spin_to(pivot, -90) #starting pos must be w brain on right side & pivot motor on right side
    # for 3:7 ratio
    if n == 0: # dock
        table.spin_to_position(420, DEGREES, 75, RPM)
        pivot.spin_to_position(0, DEGREES, 40, RPM)
    elif n == 1: # end
        table.spin_to_position(420, DEGREES, 75, RPM)
        pivot.spin_to_position(180, DEGREES, 40, RPM)
    elif n == 2: # park
        table.spin_to_position(210, DEGREES, 75, RPM)
    table.reset_position()

def manual_reset():
    # manually return to neutral position then activate
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

def auto_drive(target, max = 100):
    LB.reset_position()
    LF.reset_position()
    RB.reset_position()
    RF.reset_position()
    # gains for pct/in although percent of 100 rpm literally is just rpm huh
    p_g = 6
    i_g = 0.01
    d_g = 3.44

    err = target
    p_err = target
    while err < 0.1:
        curr = 3.25*(LB.position(TURNS) + LF.position(TURNS) + RB.position(TURNS) + RF.position(TURNS)) / 4
        err = target - curr
        p = p_g*err
        i += i_g*err*100
        d = d_g*(err-p_err) / 100

        p_err = err
        spd = p + i + d
        if spd > max:
            drive(max, max, RPM)
        else:
            drive(spd, spd, PERCENT)

        wait(100, MSEC)
    wait(300, MSEC)

def auto_turn(target, max = 100):
    inert.reset_rotation()
    # gains for pct/in
    p_g = 0.3
    i_g = 0
    d_g = 0.15

    err = target
    p_err = target
    while err < 0.1:
        curr = inert.rotation()
        err = target - curr
        p = p_g*err
        i += i_g*err*100
        d = d_g*(err-p_err) / 100

        p_err = err
        spd = p + i + d
        if spd > max:
            drive(-max, max, RPM)
        else:
            drive(-spd, spd, PERCENT)

        wait(100, MSEC)
    wait(300, MSEC)

def autonomous():
    

def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

def user_control():
    pivot.set_timeout(2, SECONDS)
    device_check()
    ax2 = 0
    ax3 = 0
    table_tog = 0
    # place driver control in this while loop
    while True:
        # action hotkeys
        if controller.buttonX.pressing():
            switch(0)
        if controller.buttonA.pressing():
            switch(1)
        if controller.buttonY.pressing():
            switch(2)

        # control
        if controller.buttonLeft.pressing():
            manual_reset()
        if controller.buttonUp.pressing():
            table_tog += 1

        # manual adjust
        if controller.buttonR1.pressing():
            pivot.spin(FORWARD, 15)
        elif controller.buttonR2.pressing():
            pivot.spin(FORWARD, -15)
        else:
            pivot.stop(HOLD)
        if controller.buttonL1.pressing():
            if (table_tog/2) - math.floor(table_tog/2) > 0:
                table.spin(FORWARD, 100)
            else:
                belt(75)
        elif controller.buttonL2.pressing():
            if (table_tog/2) - math.floor(table_tog/2) > 0:
                table.spin(FORWARD, -100)
            else:
                belt(-75)
        else:
            belt_brake()
            table.stop(HOLD)

        ax3 = controller.axis3.position()
        ax2 = controller.axis2.position()

        if abs(ax3) > 2 or abs(ax2) > 2:
            drive(curve(ax3), curve(ax2), RPM)
        else:
            brake(BRAKE)
        wait(20, MSEC)
        # t += 20
        # if (t/500) == math.floor(t/500):
        #     print("curr: ", table.current())
        #     print("power: ", table.power())
        #     print("torq: ", table.torque())
        #     print("eff: ", table.efficiency())
        #     print("temp: ", table.temperature())
        #     print()


# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()