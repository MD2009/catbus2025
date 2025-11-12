from vex import *

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
