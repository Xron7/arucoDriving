from controller import *
import cv2
import numpy as np

robot = Robot()
t90=44
timestep = int(robot.getBasicTimeStep())
#-----------------------------------------
#ΣΥΝΔΕΣΗ ΚΑΙ ΑΡΧΙΚΟΠΟΙΗΣΗ
camera=robot.getCamera("camera")
camera.enable(timestep)
height=camera.getHeight()
width=camera.getWidth()

leftMotor = robot.getMotor("left wheel motor")
rightMotor = robot.getMotor("right wheel motor")
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

#-------------------------------------------
#ΠΑΡΑΜΕΤΡΟΙ ΓΙΑ goodFeatures και Optical Flow
number_of_features=50
quality=0.1
eucldis=10
collisiontime=0
lk_params = dict( winSize  = (5,5),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
#-----------------------------------------
#ΣΥΝΑΡΤΗΣΕΙΣ
init=0
speed=4
def create_image():

    cameraData=camera.getImage()
    image=np.frombuffer(cameraData, np.uint8).reshape((height, width, 4))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return gray




def calc_hypotenuse(f1,f2):
    
    return ((f1[0]-f2[0])**(2)+(f1[1]-f2[1])**(2))**(0.5)
#-----------------------------------------
#ΦΙΛΤΡΑΡΙΣΜΑ
def Filter_enormous_hypotenuse(frame1_features,frame2_features):
    tmp=0
    for i in range(len(frame1_features)):        
        hypotenuse = calc_hypotenuse(frame1_features[i][0],frame2_features[i][0])
        
        if (hypotenuse < 300): 
            frame1_features[tmp][0][0] = frame1_features[i][0][0]
            frame1_features[tmp][0][1] = frame1_features[i][0][1]
            frame2_features[tmp][0][0] = frame2_features[i][0][0]
            frame2_features[tmp][0][1] = frame2_features[i][0][1]
            tmp+=1
    return frame1_features,frame2_features,tmp
    
sumflow=0
countflow=0    
def estimate_mean_flow(frame1_features,frame2_features,number_of_features,countflow,sumflow):
    
    for i in range(len(frame1_features)): 
        hypotenuse = calc_hypotenuse(frame1_features[i][0],frame2_features[i][0])
        
        countflow+=1;
        sumflow += hypotenuse;
    meanflow=sumflow/countflow
    return meanflow,countflow,sumflow
    
    
def mean_flow_filter(frame1_features,frame2_features,number_of_features,meanflow):
    tmp=0
    
    for i in range(len(frame1_features)):
        hypotenuse = calc_hypotenuse(frame1_features[i][0],frame2_features[i][0])
        if (meanflow!=0 and hypotenuse/meanflow < 120): 
            frame1_features[tmp][0][0] = frame1_features[i][0][0]
            frame1_features[tmp][0][1] = frame1_features[i][0][1]
            frame2_features[tmp][0][0] = frame2_features[i][0][0]
            frame2_features[tmp][0][1] = frame2_features[i][0][1]
            tmp+=1
    return frame1_features,frame2_features,tmp
#-----------------------------------------
#ΜΕΤΡΗΣΗ ΡΟΗΣ    
def count_flow(frame1_features,frame2_features,number_of_features,collisiontime):
    skycount=0
    sumskycountx=0
    sumskycounty=0
    leftgroundcount=0
    sumleftcountx=0
    sumleftcounty=0
    rightgroundcount=0
    sumrightcountx=0
    sumrightcounty=0
    collisioncount=0
    sumcollisiontime=0
    for i in range(number_of_features):
        px=frame1_features[i][0][0]
        py=frame1_features[i][0][1]
        qx=frame2_features[i][0][0]
        qy=frame2_features[i][0][1]
        
        if py<height*2/7:
            skycount+=1
            sumskycountx+=(px-qx)
            sumskycounty+=(py-qy)
        elif px<width/2:
            leftgroundcount+=1
            sumleftcountx+=(px-qx)
            sumleftcounty+=(py-qy)
        else:
            rightgroundcount+=1
            sumrightcountx+=(px-qx)
            sumrightcounty+=(py-qy)
            
        if py>height*2/7 and px>width*2/7 and py<height*5/7 and px<width*5/7:
            collisioncount+=1
            sumcollisiontime+=(py-qy)            
            if collisioncount!=0:
                collisiontime+=sumcollisiontime/collisioncount
        
    return skycount,sumskycountx,sumskycounty,leftgroundcount,sumleftcountx,sumleftcounty,rightgroundcount,sumrightcountx,sumrightcounty,collisiontime
#-----------------------------------------
#ΦΙΛΤΡΑΡΙΣΜΑ ΤΑΛΑΝΤΩΣΕΩΝ    
skyrotationx=0
skyrotationy=0
def rotation_handling(sumskycountx,sumskycounty,skycount,height,width,skyrotationx,skyrotationy):
    if skycount!=0:
        skyrotationx+=(sumskycountx/skycount)
        skyrotationy+=(sumskycounty/skycount)
    #px=width/2
    #py=height/7
    #qx=px+skyrotationx
    #qy=py+skyrotationy
    
    return skyrotationx,skyrotationy

lgtx=0
rgtx=0
lgty=0
rgty=0
def translation_handling(slcx,slcy,lgc,srcx,srcy,rgc,srx,sry,height,width,lgtx,rgtx,lgty,rgty):
    if lgc!=0:
        lgtx+=(slcx/lgc)
        lgty+=(slcy/lgc)
    #px=width/4
    #py=height*6/7
    #qx=px+lgtx-srx
    #qy=py+lgty-sry
    if rgc!=0:
        rgtx+=(srcx/rgc)
        rgty+=(srcy/rgc)
    #px=width*3/4
    #py=height*6/7
    #qx=px+rgtx-srx
    #qy=py+rgty-sry
    
    return lgtx,lgty,rgtx,rgty
#-----------------------------------------
#ΥΠΟΛΟΓΙΣΜΟΣ ΡΟΗΣ    
flowlefttotal=0
flowrighttotal=0
def calc_flow(lgtx,lgty,rgtx,rgty,srx,sry,flowlefttotal,flowrighttotal):
    trleftx = lgtx -srx
    trlefty = lgty-sry
    trrightx = rgtx-srx
    trrighty = rgty-sry
    
    flowleft=-(trleftx-srx)
    flowright=trrightx-srx
    flowlefttotal+=abs(flowleft)
    flowrighttotal+=abs(flowright)
    
    return flowlefttotal,flowrighttotal
#-----------------------------------------
#ΣΥΝΑΡΤΗΣΕΙΣ ΚΙΝΗΣΗΣ
def move_forw(speed):
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)

    return None
    
def turn(speed,dir):
    if dir==0:
        leftMotor.setVelocity(-speed)
        rightMotor.setVelocity(speed)
    else:
        leftMotor.setVelocity(speed)
        rightMotor.setVelocity(-speed)
        
    return None

def stop():
    move_forw(0)
    return None
#-----------------------------------------
def decide(lf,rf):
    if lf>rf:
        return 1
    else:
        return 0
#---------------------------------------------
#ΤΟ ΛΟΥΠ
flag=0
while robot.step(timestep) != -1:

    if init==0:
        gray1=create_image()
        init=1
            
    if flag==0:
        #ΕΠΕΞΕΡΓΑΣΙΑ
        frame1_features=cv2.goodFeaturesToTrack(gray1,number_of_features,quality,eucldis)
        gray2=create_image()
        if np.any(frame1_features):
            frame2_features = cv2.calcOpticalFlowPyrLK(gray2,gray1,frame1_features, None,**lk_params)
            frame2_features=frame2_features[0]
            
            frame1_features,frame2_features,newnumoffeatures=Filter_enormous_hypotenuse(frame1_features,frame2_features)
            meanflow,countflow,sumflow=estimate_mean_flow(frame1_features,frame2_features,newnumoffeatures,countflow,sumflow)
            frame1_features,frame2_features,newnumoffeatures=mean_flow_filter(frame1_features,frame2_features,number_of_features,meanflow)
            
            skycount,sumskycountx,sumskycounty,leftgroundcount,sumleftcountx,sumleftcounty,rightgroundcount,sumrightcountx,sumrightcounty,collisiontime=count_flow(frame1_features,frame2_features,newnumoffeatures,collisiontime)
            
            skyrotationx,skyrotationy= rotation_handling(sumskycountx,sumskycounty,skycount,height,width,skyrotationx,skyrotationy)
            lgtx,lgty,rgtx,rgty=translation_handling(sumleftcountx,sumleftcounty,leftgroundcount,sumrightcountx,sumrightcounty,rightgroundcount,skyrotationx,skyrotationy,height,width,lgtx,rgtx,lgty,rgty)
            
            flowlefttotal,flowrighttotal=calc_flow(lgtx,lgty,rgtx,rgty,skyrotationx,skyrotationy,flowlefttotal,flowrighttotal)
        
        #-----------------------------------------------------------------------------------------------------------------
        move_forw(speed)
    
        print(collisiontime)
        
        if collisiontime<-3:
            stop()
            flag=1
            dir=decide(flowlefttotal,flowrighttotal)
            flowlefttotal=0
            flowrighttotal=0
            collisiontime=0
            time=t90
    else:
        if time>0:
            turn(speed,dir)
            time-=1
        else:
            flag=0
        
    gray1=gray2
    
    
    
    pass