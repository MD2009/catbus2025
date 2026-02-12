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

belt1 = Motor(Ports.PORT10)
belt2 = Motor(Ports.PORT8)
pivot = Motor(Ports.PORT9)
table = Motor(Ports.PORT7)

RF = Motor(Ports.PORT5)
RB = Motor(Ports.PORT4)
LF = Motor(Ports.PORT2)
LB = Motor(Ports.PORT3)

inert = Inertial(Ports.PORT1)
dock1 = Bumper(brain.three_wire_port.a)
dock2 = Bumper(brain.three_wire_port.b)

# driver
def curve(x):
    return pow(x, 2)/100 * (x/abs(x)) * 0.25

def drive(Rspd, Lspd, type):
    LF.spin(FORWARD, -Lspd, type)
    LB.spin(FORWARD, -Lspd, type)
    RF.spin(FORWARD, Rspd, type)
    RB.spin(FORWARD, Rspd, type)
    print((3.25*(-LB.position() - LF.position() + RB.position() + RF.position())) / (4*360))

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

switch_cnt = 1

def switch(n):
    # full rotation = 180, half = 90, a lot more accurate now w/ high srth axle & motor
    t = 0
    global switch_cnt
    if dock1.pressing():
        save = True
    elif dock2.pressing():
        save = False
    pivot.spin_to_position(135)
    # spin_to(pivot, -90) #starting pos must be w brain on right side & pivot motor on left side
    # for 3:7 ratio
    if n == 0: # dock
        table.spin_to_position(420*switch_cnt)
        while not dock1.pressing() and not dock2.pressing() and t < 2:
            if save:
                pivot.spin(FORWARD, 40*switch_cnt)
            else:
                pivot.spin(REVERSE, 40*switch_cnt)
            wait(20, MSEC)
            t += 0.01
        pivot.stop()
    elif n == 1: # end
        table.spin_to_position(420*switch_cnt)
        while not dock1.pressing() and not dock2.pressing() and t < 2:
            if save:
                pivot.spin(REVERSE, 40*switch_cnt)
            else:
                pivot.spin(FORWARD, 40*switch_cnt)
            wait(20, MSEC)
            t += 0.01
        pivot.stop()
    elif n == 2: # park
        table.spin_to_position(105)
    elif n == 3: # center goal
        wait(5, MSEC)
    elif n == 4: # return
        table.spin_to_position(0)
        while not dock1.pressing() and not dock2.pressing() and t < 2:
            pivot.spin(FORWARD)
            wait(10, MSEC)
            t += 0.01
        pivot.stop()
    table.reset_position()
    if switch_cnt > 0:
        switch_cnt -= 2
    else:
        switch_cnt += 2

def manual_reset():
    # manually return to neutral position then activate
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

# def auto_drive(target, max = 100):
#     LB.reset_position()
#     LF.reset_position()
#     RB.reset_position()
#     RF.reset_position()
#     # gains for pct/in although percent of 100 rpm literally is just rpm huh
#     p_g = 6
#     i_g = 0.01
#     d_g = 3.44
    
#     i = 0
#     err = target
#     p_err = target
#     while abs(err) > 0.1:
#         curr = 3.25*RB.position(TURNS)
#         err = target - curr
#         p = p_g*err
#         i += i_g*err*100
#         d = d_g*(err-p_err) / 100

#         p_err = err
#         spd = p + i + d
#         if abs(spd) > max:
#             drive(max, max, RPM)
#         else:
#             drive(spd, spd, PERCENT)

#         print("Current: ", curr)
#         print("Error: ", err)
#         print("Speed: ", spd)
#         wait(100, MSEC)
#     wait(300, MSEC)

# def auto_turn(target, max = 100):
#     inert.reset_rotation()
#     # gains for pct/in
#     p_g = 0.3
#     i_g = 0
#     d_g = 0.15

#     err = target
#     p_err = target
#     while abs(err) > 0.1:
#         curr = inert.rotation()
#         err = target - curr
#         p = p_g*err
#         i += i_g*err*100
#         d = d_g*(err-p_err) / 100

#         p_err = err
#         spd = p + i + d
#         if spd > max:
#             drive(-max, max, RPM)
#         else:
#             drive(-spd, spd, PERCENT)

#         wait(100, MSEC)
#     wait(300, MSEC)

def auto_drive():
    

def autonomous():
    # auto_drive(36, 40)
    # auto_turn(-90, 80)
    # auto_drive(-20, 60)
    # belt(80)
    wait(5, SECONDS)
    belt_brake()
    
def device_check():
    if LF.installed() and RF.installed() and LB.installed() and RB.installed():
        controller.rumble('_')
    else:
        controller.screen.print("device discon")
        controller.rumble('...')

table_t = 0
def test():
    global table_t
    table_t += 1

controller.buttonUp.pressed(test)

def user_control():
    global table_t
    table.set_velocity(75, RPM)
    table.set_timeout(3, SECONDS)
    pivot.set_velocity(40, RPM)
    device_check()
    # place driver control in this while loop
    while True:
        # action hotkeys
        if controller.buttonA.pressing():
            switch(0)
        if controller.buttonB.pressing():
            switch(1)
        if controller.buttonRight.pressing():
            switch(2)
        if controller.buttonY.pressing():
            switch(3)
        if controller.buttonX.pressing():
            switch(4)

        # control
        if controller.buttonLeft.pressing():
            manual_reset()

        # manual adjust
        if controller.buttonR1.pressing():
            pivot.spin(FORWARD, 15)
        elif controller.buttonR2.pressing():
            pivot.spin(FORWARD, -15)
        else:
            pivot.stop(HOLD)
        if controller.buttonL1.pressing():
            if (table_t/2) - math.floor(table_t/2) > 0:
                table.spin(FORWARD)
            else:
                belt(100)
        elif controller.buttonL2.pressing():
            if (table_t/2) - math.floor(table_t/2) > 0:
                table.spin(REVERSE)
            else:
                belt(-100)
        else:
            belt_brake()
            table.stop(HOLD)

        ax3 = controller.axis3.position()
        ax2 = controller.axis2.position()

        if abs(ax3) > 1 or abs(ax2) > 1:
            drive(ax2, ax3, RPM)
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