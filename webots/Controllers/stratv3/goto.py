from controller import *

robot = Robot()

timestep = int(robot.getBasicTimeStep()) 
speed=4
step=3

halfc=98
quarterc=49
fullc=196

leftMotor = robot.getMotor("left wheel motor")
rightMotor = robot.getMotor("right wheel motor")
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)


tstop=[[0,quarterc,halfc,quarterc],[quarterc,0,quarterc,halfc],[halfc,quarterc,0,quarterc],[quarterc,halfc,quarterc,0]]
tstr=[[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]]

def nextdir(currentpos,nextpos,currentdir,tstop,tstr):
    if currentpos[0]<nextpos[0]:
        nextdir=2
    elif currentpos[0]>nextpos[0]:
        nextdir=0
    else:
        if currentpos[1]<nextpos[1]:
            nextdir=1
        else:
            nextdir=3
    
    stop=tstop[currentdir][nextdir]
    str=tstr[currentdir][nextdir]
    
    return stop,str,nextdir
            
            
def turn(str):
    if str==1:
        leftspeed=speed/2
        rightspeed=-speed/2
    else:
        leftspeed=-speed/2
        rightspeed=speed/2
    leftMotor.setVelocity(leftspeed)
    rightMotor.setVelocity(rightspeed)
    return None

def move(speed):
    leftspeed=speed
    rightspeed=speed
    leftMotor.setVelocity(leftspeed)
    rightMotor.setVelocity(rightspeed)
    return None




