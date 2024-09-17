import numpy as np
import cv2
import cv2.aruco as aruco
#import motorfunctions

#ΑΡΧΙΚΟΠΟΙΗΣΗ
close=150
centerleft=280
centerright=320
goal=2#Ο ΑΡΙΣΜΟΣ ΤΟΥ ΤΕΡΜΑΤΙΣΜΟΥ
cap = cv2.VideoCapture(0)
counter=0
turndir=0
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
mode=0

#ΣΥΝΑΡΤΗΣΗ ΛΗΨΗΣ ΕΙΚΟΝΑΣ ΚΑΙ ΜΕΤΑΤΡΟΠΗΣ ΣΕ ΓΚΡΙ
def getimage():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame,gray

    
while(1):
    
    #ΛΑΜΒΑΝΩ ΕΙΚΟΝΑ,ΤΗΝ ΚΑΝΩ ΓΚΡΙ ΚΑΙ ΨΑΧΝΩ ARUCO
    frame,gray=getimage()
    res = cv2.aruco.detectMarkers(gray,dictionary)
    
    if mode==0:#ΨΑΧΝΩ ΓΙΑ ARUCO
        
        print('ΨΑΧΝΩ')
        #motorfunctions.turn_left()      

        #ΑΝ ΒΡΗΚΑ 
        if len(res[0])>0:
            current=res[1][0][0]#ΤΟ ΟΡΙΖΩ ΩΣ ΤΡΕΧΟΝ
            n=0
            for i in range(len(res[1])):
                if current<res[1][i][0] and counter<res[1][i][0]:
                    current=res[1][i][0]
                    n=i
            if current>counter:
                counter=current
                print('ΒΡΗΚΑ!')
                mode=1
                #motorfunctions.stop()
            
    elif mode==1:#ΕΧΩ ΒΡΕΙ ARUCO ΚΑΙ ΠΑΩ ΠΡΟΣ ΑΥΤΟ
        
        #ΠΛΗΣΙΑΖΩ ΚΑΙ ΚΕΝΤΡΩΝΩ
        cm=0
        if len(res[0]) > 0:#Ο ΕΛΕΓΧΟΣ ΕΔΩ ΕΙΝΑΙ ΓΙΑ ΤΗΝ ΑΠΟΦΥΓΗ ERRORS
                           #ΟΤΑΝ ΕΝΤΟΠΙΖΟΝΤΑΙ ΠΟΛΛΟΙ ΔΕΙΚΤΕΣ 
            for i in range(len(res[0])):
                if current==res[1][i][0]:
                    cm=1
                    break
        if cm==1:
            print('Current Marker:',current)
            res2=res[0][n][0]
            dis=abs(res2[0][1]-res2[3][1])
            print(dis)
            
            if dis<close:
                midx=0.5*(res2[0][0]+res2[1][0])
                
                if midx<centerleft:
                    
                    print('ΣΤΡΙΒΩ ΑΡΙΣΤΕΡΑ')
                    #motorfunctions.turn_left()
                    turndir=0
                    
                elif midx>centerright:
                    
                    print('ΣΤΡΙΒΩ ΔΕΞΙΑ')
                    #motorfunctions.turn_right()
                    turndir=1
                    
                else:
                    
                    print('ΠΛΗΣΙΑΖΩ')
                    #motorfunctions.move_forw()
            else:
                if current==goal:
                    mode=3
                else:
                    mode=0
                print('ΕΦΤΑΣΑ')
                #motorfunctions.stop()
        else:
            mode=2
            
    #ΑΝ ΧΑΘΗΚΕ ΤΟ ΤΡΕΧΟΝ       
    elif mode==2:#ΨΑΧΝΩ ΤΟ ΧΑΜΕΝΟ ARUCO
        
        print("ΕΧΑΣΑ ΤΟ MARKER, ΞΑΝΑΨΑΧΝΩ")
        if turndir==0:
            
            print("ΣΤΡΙΒΩ ΔΕΞΙΑ")
            #motorfunctions.turn_right()
        else:
            print("ΣΤΡΙΒΩ ΑΡΙΣΤΕΡΑ")
            #motorfunctions.turn_left()
        
        if len(res[0])>0:
             for i in range(len(res[1])):
                 if counter==res[1][i][0]:
                     
                     mode=1
                     break
                  
    else:#ΤΕΡΜΑΤΗΣΑ      
        print('ΤΕΛΟΣ!!!!!!!!!!!')
        motorfunctions.stop()
        break
        
    if len(res[0]):
        cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
        
    cv2.imshow('Live Feed',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        #motorfunctions.stop()
        break

#motorfunctions.clean()
cap.release()
cv2.destroyAllWindows()
