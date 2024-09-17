from controller import *
import numpy as np
robot = Robot()

timestep = int(robot.getBasicTimeStep()) 
speed=4
step=3

t45=25
t180=98
t90=49
t360=196

leftMotor = robot.getMotor("left wheel motor")
rightMotor = robot.getMotor("right wheel motor")
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

tstop=np.zeros((8,8),dtype=int)
turns=[0,t45,t90,t45+t90,t180,t45+t90,t90,t45]
for i in range(8):
    for j in range(8):
            tstop[i,(i+j)%8]=turns[j]
tstr=np.zeros((8,8),dtype=int)
for i in range(8):
    for j in range(4):
        tstr[i,(i+j+1)%8]=1


pool=[[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
def nextdir(currentpos,nextpos,currentdir,tstop,tstr):
    
    nextdir=pool.index([np.sign(nextpos[0]-currentpos[0]),np.sign(nextpos[1]-currentpos[1])])
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




