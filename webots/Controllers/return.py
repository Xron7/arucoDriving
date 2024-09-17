from controller import *

robot = Robot()

timestep = int(robot.getBasicTimeStep())

class Switcher(object):
          def indirect(self,i):
                   method_name='number_'+str(i)
                   method=getattr(self,method_name,lambda :'Invalid')
                   return method()
          def number_0(self):
                   return 'zero'
          def number_1(self):
                   return 'one'
          def number_2(self):
                   return 'two'

def color(image, width, height):
    for i in range(width/3, 2*width/3+1):
        for j in range(height/3, 2*height/3+1):
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
          
              
    return current_blob

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
stop=40
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
            leftspeed=speed
            rightspeed=speed
            if blob!="none":
                print(blob,"blob found")
        else:
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

        if blob=target:
            mode=3

        if blob!="none":
            print(blob,"blob found")
            
    pass
