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

def createpath(s,g):
    start=(int(100*s[0]+44),int(44-100*s[1]))
    goal=(int(100*g[0]+44),int(44-100*g[1]))
    #start=(14,14)
    #goal=(32,16)
    came_from = a_star_search(diagram4, start, goal)
    path=reconstruct_path(came_from,start,goal)
    print(path)
    if path[0][0]==path[1][0]:
        b=0
    elif path[0][1]==path[1][1]:
        b=2
    else:
        if np.sign(path[0][0]-path[1][0])==np.sign(path[0][1]-path[1][1]):
            b=3
        else:
            b=1
    path2=[]
    path2.append(path[0])
    i=1
    j=0
    c=[1]
    while i<len(path)-1:
        if path[i][0]==path[i+1][0]:
            d=0
        elif path[i][1]==path[i+1][1]:
            d=0
        else:
            if np.sign(path[i][0]-path[i+1][0])==np.sign(path[i][1]-path[i+1][1]):
                d=3
            else:
                d=1
            
        if d==b:
            c[j]+=1
            i+=1
        else:
            path2.append(path[i])
            c.append(0)
            j+=1
            b=d
    path2.append(path[len(path)-1])
    path=path2
    dire=[2]
    stop=[]
    str=[]

    for i in range(len(path)-1):
        s,st,d=nextdir(path[i],path[i+1],dire[i],tstop,tstr)
        stop.append(s)
        str.append(st)
        dire.append(d)
    for i in range(len(c)):
        if dire[i+1]==3 or dire[i+1]==1:
            c[i]=1.414*c[i]
    return path,stop,str,dire,c


ds0 = robot.getDistanceSensor("ds0")
ds1 = robot.getDistanceSensor("ds1")
ds0.enable(timestep)
ds1.enable(timestep)

camera=robot.getCamera("camera")
camera.enable(timestep)
width=camera.getWidth()
height=camera.getHeight()


start, goal = (-0.44, 0.44), (0,0)
path,stop,str,dire,c=createpath(start,goal)
print(path)
i=0
dis=c[i]*step
while robot.step(timestep) != -1:
    
    if i<len(path)-1:   
        if stop[i]!=0:
            stop[i]-=1
            turn(str[i])
        else:
            if dis>0:
                dis-=1
                move(speed)
                
            else:
                i+=1
                if i<len(path)-1:            
                    dis=c[i]*step
                else:
                    move(0)
                    break
    pass