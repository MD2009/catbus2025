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

# driver
switch_cnt = 0

def curve(x):
    return pow(x, 2)/100 * (x/abs(x)) * 0.5

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
    # full rotation = 180, half = 90, a lot more accurate now w/ high srth axle & motor
    pivot.spin_to_position(-90, DEGREES, 40, RPM)
    # spin_to(pivot, -90) #starting pos must be w brain on right side & pivot motor on right side
    if n == 0: # dock
        table.spin_to_position(1260, DEGREES, 75, RPM)
        pivot.spin_to_position(0, DEGREES, 40, RPM)
    elif n == 1: # end
        table.spin_to_position(1260, DEGREES, 75, RPM)
        pivot.spin_to_position(180, DEGREES, 40, RPM)
    elif n == 2: # park
        table.spin_to_position(630, DEGREES, 75, RPM)
    table.reset_position()

def manual_reset():
    # manually return to neutral position then activate
    pivot.stop(HOLD)
    table.stop(HOLD)
    pivot.reset_position()
    table.reset_position()

# auto
posY = 0.0
posX = 0.0

def auto_drive(dir, pos):
    t = 0
    if dir == "fb":
        global posY
        dif1 = pos-posY
        dif = dif1
        while math.fabs(dif) > 0.1 and t < dif1*0.1: #timeout, abt 10in/sec?
            acc_i = .393700787*inert.acceleration(XAXIS)
            drive_FB((dif/dif1)*100) # percent of distance incompleted, 
            print((dif/dif1)*100)
            wait(10, MSEC)
            acc_f = .393700787*inert.acceleration(XAXIS) # convert to in
            avg_spd = (acc_f-acc_i)/0.01 # find avg rate of change of acc
            posY += avg_spd*0.01
            dif = pos-posY
            t += 0.01
    elif dir == "lr":
        global posX
        dif1 = pos-posX
        dif = dif1
        while math.fabs(dif) > 0.1 and t < dif1*0.1:
            acc_i = .393700787*inert.acceleration(ZAXIS)
            drive_LR((dif/dif1)*100)
            wait(10, MSEC)
            acc_f = .393700787*inert.acceleration(ZAXIS)
            posX += acc_f-acc_i #i guess i literally couldve just simplified it to that whoops
            dif = pos-posX
            t += 0.01
    elif dir == "rot":
        dif1 = pos-inert.heading()
        dif = dif1
        while math.fabs(dif) > 0.1 and t < dif1/720: # 2 revs/sec?
            drive_rot((dif/dif1)*100)
            wait(10, MSEC)
            dif = pos-inert.heading()
            t += 0.01
    brake(BRAKE)
    belt_brake()
    wait(500, MSEC)

def autonomous():
    auto_drive("lr", -50)  # left by a chunk of range
    auto_drive("fb", 35)  # forward by a chunk of range
    belt(-70)  # who knows, just dump
    wait(900, MSEC)  # wait
    belt_brake()
    wait(1500, MSEC)  # score!

def autonomous_old():
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
    wait(2000,MSEC)
    device_check()
    ax1 = 0
    ax2 = 0
    ax3 = 0
    ax4 = 0
    t = 0
    # place driver control in this while loop
    while True:
        # action hotkeys
        if controller.buttonX.pressing():
            switch(0)
        if controller.buttonA.pressing():
            switch(1)
        if controller.buttonUp.pressing():
            switch(2)
        if controller.buttonB.pressing():
            auto_drive("fb", 10)

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
            table.spin(FORWARD, 75)
        elif controller.buttonL2.pressing():
            table.spin(FORWARD, -75)
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

        if abs(ax3) > 5:
            drive_FB(ax3)
        elif abs(ax4) > 1:
            drive_LR(ax4)
        elif abs(ax1) > 1:
            drive_rot(ax1)
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