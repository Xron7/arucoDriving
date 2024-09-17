from controller import *

robot = Robot()

timestep = int(robot.getBasicTimeStep()) 


def color(image, width, height):
    red=0
    blue=0
    green=0
    for i in range(int(width/3), int(2*width/3+1)):
        for j in range(int(height/3), int(2*height/3+1)):
            
            red+= Camera.imageGetRed(image,width,i,j)
            blue+= Camera.imageGetBlue(image,width,i,j)
            green+= Camera.imageGetGreen(image,width,i,j)

    if red > 3 * green and red > 3 *blue :
        blob = "red"
    elif green > 3 * red and green> 3 * blue :
        blob = "green"
    elif blue > 3 * red and blue > 3 * green :
        blob = "blue"
    else: blob = "none"
          
              
    return blob

gps=robot.getGPS("gps")
gps.enable(timestep)

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

speed=4
stop=195
mode=1
target="green"
while robot.step(timestep) != -1:
    
    image=camera.getImage()

    if mode==1:
        
        if stop!=0:
            blob=color(image,width,height)
            if blob==target:
                mode=3
            stop-=1
            leftspeed=-speed
            rightspeed=speed
            if blob!="none":
                print(blob,"blob found")
        else:
            time=1000
            mode=2

    elif mode==2:
        
        ds0value=ds0.getValue()
        ds1value=ds1.getValue()
        image=camera.getImage()

        if ds1value>500:
            if ds0value>500:
                leftspeed=-speed
                rightspeed=-speed
            else:
                leftspeed = -ds1value / 100
                rightspeed = (ds0value / 100) + 0.5
        elif ds0value>500:
            leftspeed = (ds1value / 100) + 0.5
            rightspeed = -ds0value / 100
        else:
            leftspeed=speed
            rightspeed=speed

        blob=color(image,width,height)

        if blob==target:
            mode=3

        if blob!="none":
            print(blob,"blob found")
         
        time-=1
        if time==0:
            stop=97
            mode=1
            

    elif mode==3:
        leftspeed=0
        rightspeed=0
        print("target",blob,"found")
        mode=4
    else:
        pass
    print(gps.getValues())
    leftMotor.setVelocity(leftspeed)
    rightMotor.setVelocity(rightspeed)
    
    pass
