#ΕΙΣΑΓΩΓΗ ΒΙΒΛΙΟΘΗΚΩΝ
import numpy as np
import cv2
#import motorfunctions#ΣΥΝΑΡΤΗΣΕΙΣ ΚΙΝΗΣΗΣ

#ΑΡΧΙΚΟΠΟΙΗΣΗ
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 160)
video_capture.set(4, 120)

dexioorio=160#160 για webcam, 120 για PiCamera
aristeroorio=90#90 για webcam, 50 για PiCamera
turndir=1

lower_white = np.array([0, 0, 212])
upper_white = np.array([131, 255, 255])

while(True): 

    # ΠΑΙΡΝΩ FRAME
    ret, frame = video_capture.read()
    #cv2.imshow('frame',frame)
    
    # ΠΕΡΙΚΟΠΗ
    #crop_img = frame[60:120, 0:160]#PiCamera
    crop_img = frame[120:210, 0:320]#Webcam
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_RGB2HSV)

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Remove noise
    kernel_erode = np.ones((4,4), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((6,6),np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    # Find the different contours
    contours,_ = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area (keep only the biggest one)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    if len(contours) > 0:
        M = cv2.moments(contours[0])
        # Centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        

        #ΣΧΕΔΙΑΣΗ
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1) 

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
        
        #ΑΠΟΦΑΣΗ ΚΙΝΗΣΗΣ
        if cx >= dexioorio:

            print ("ΣΤΡΙΒΩ ΔΕΞΙΑ")
            #motorfunctions.turn_right()
            turndir=1
        elif cx < dexioorio and cx > aristeroorio:

            print ("ΠΡΟΧΩΡΑΩ")
            #motorfunctions.move_forw()
            turndir=0
            
        elif cx <= aristeroorio:
            print ("ΣΤΡΙΒΩ ΑΡΙΣΤΕΡΑ")
            #motorfunctions.turn_left()
            turndir=0

    else:#ΑΝ ΧΑΘΕΙ Η ΓΡΑΜΜΗ
        
        print ("ΨΑΧΝΩ ΓΙΑ ΤΗ ΓΡΑΜΜΗ")
        if turndir==0:
            print("ΣΤΡΙΒΩ ΔΕΞΙΑ")
            #motorfunctions.turn_right()
        else:
            print("ΣΤΡΙΒΩ ΑΡΙΣΤΕΡΑ")
            #motorfunctions.turn_left()

    #ΠΡΟΒΟΛΗ ΕΙΚΟΝΑΣ

    cv2.imshow('frame',crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):#ΣΤΑΜΑΤΑΩ
        
        #motorfunctions.stop()
        break
    
#motorfunctions.clean()#ΑΠΟΔΕΣΜΕΥΣΗ ΤΩΝ PINS
video_capture.release()
cv2.destroyAllWindows()
