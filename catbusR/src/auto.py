from driver import *

posY = 0.0
posX = 0.0

def auto_drive(dir, pos):
    if dir == "fb":
        global posY
        dif1 = pos-posY
        dif = dif1
        while math.fabs(dif) > 0.1:
            acc_i = .393700787*inert.acceleration(ZAXIS)
            drive_FB(dif/dif1) # percent of distance incompleted, 
            wait(10, MSEC)
            acc_f = .393700787*inert.acceleration(ZAXIS) # convert to in
            avg_spd = (acc_f-acc_i)/0.01 # find avg rate of change of acc
            posY += avg_spd*0.01
            dif = pos-posY
    elif dir == "lr":
        global posX
        dif1 = pos-posX
        dif = dif1
        while math.fabs(dif) > 0.1:
            acc_i = .393700787*inert.acceleration(XAXIS)
            drive_LR(dif/dif1)
            wait(10, MSEC)
            acc_f = .393700787*inert.acceleration(XAXIS)
            posX += acc_f-acc_i #i guess i literally couldve just simplified it to that whoops
            dif = pos-posX
    elif dir == "rot":
        dif1 = pos-inert.heading()
        dif = dif1
        while math.fabs(dif) > 0.1:
            drive_rot(dif/dif1)
            wait(10, MSEC)
            dif = pos-inert.heading()
    brake(BRAKE)
    belt_brake()
    print("LF: ", LF.position(TURNS))
    print("RF: ", RF.position(TURNS))
    print("LB: ", LB.position(TURNS))
    print("RB: ", RB.position(TURNS))
    wait(500, MSEC)