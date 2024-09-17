from controller import *

robot = Robot()

timestep = int(robot.getBasicTimeStep()) 
speed=4
step=10

halfc=98
quarterc=49
fullc=196

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






ds0 = robot.getDistanceSensor("ds0")
ds1 = robot.getDistanceSensor("ds1")
ds0.enable(timestep)
ds1.enable(timestep)

camera=robot.getCamera("camera")
camera.enable(timestep)
width=camera.getWidth()
height=camera.getHeight()

leftMotor = robot.getMotor("left wheel motor")
rightMotor = robot.getMotor("right wheel motor")
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

dis=step
path=[[0,0],[0,1],[-1,1]]
dire=[0]
stop=[]
str=[]
for i in range(len(path)-1):
    s,st,d=nextdir(path[i],path[i+1],dire[i],tstop,tstr)
    stop.append(s)
    str.append(st)
    dire.append(d)
i=0
while robot.step(timestep) != -1:
    
    if i<len(path)-1:   
        if stop[i]!=0:
            stop[i]-=1
            turn(str[i])
        else:
            if dis!=0:
                dis-=1
                move(speed)
                
            else:
                i+=1            
                move(0)            
                dis=step
    pass
