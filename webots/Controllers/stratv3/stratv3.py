from astar import *
from goto import *
from controller import *


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
    
ds0 = robot.getDistanceSensor("ds0")
ds1 = robot.getDistanceSensor("ds1")
ds0.enable(timestep)
ds1.enable(timestep)

camera=robot.getCamera("camera")
camera.enable(timestep)
width=camera.getWidth()
height=camera.getHeight()



start, goal = (0, 0), (22, 17)
came_from = a_star_search(diagram4, start, goal)
path=reconstruct_path(came_from,start,goal)
if path[0][0]==path[1][0]:
    b=0
else:
    b=1
path2=[]
path2.append(path[0])
i=1
j=0
c=[1]
while i<len(path)-1:
    if path[i][b]==path[i+1][b]:
        c[j]+=1
        i+=1
    else:
        path2.append(path[i])
        c.append(0)
        j+=1
        b=(b+1)%2
path2.append(path[len(path)-1])
path=path2
dire=[1]
stop=[]
str=[]

for i in range(len(path)-1):
    s,st,d=nextdir(path[i],path[i+1],dire[i],tstop,tstr)
    stop.append(s)
    str.append(st)
    dire.append(d)

i=0
dis=c[i]*step
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
                dis=c[i]*step
    pass