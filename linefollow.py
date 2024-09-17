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
while(True): 

    # ΠΑΙΡΝΩ FRAME
    ret, frame = video_capture.read()
    #cv2.imshow('frame',frame)
    
    # ΠΕΡΙΚΟΠΗ
    #crop_img = frame[60:120, 0:160]#PiCamera
    crop_img = frame[120:210, 0:320]#Webcam
    
    # ΜΕΤΑΤΡΟΠΗ ΣΕ ΓΚΡΙ
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # ΦΙΛΤΡΑΡΙΣΜΑ
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # ΜΕΤΑΤΡΟΠΗ ΣΕ ΔΥΑΔΙΚΗ
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # ΔΙΑΒΡΩΣΗ ΚΑΙ ΔΙΑΣΤΟΛΗ
    mask = cv2.erode(thresh, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # ΕΝΤΟΠΙΣΜΟΣ ΣΧΗΜΑΤΩΝ
    contours,_ = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # ΑΝ ΒΡΗΚΑ
    if len(contours) > 0:
        
        #ΥΠΟΛΟΓΙΣΜΟΣ ΚΕΝΤΡΟΥ
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c) 
        if M['m00']!=0:#ΓΙΑ ΤΗΝ ΠΕΡΙΠΤΩΣΗ ΝΑ ΕΙΝΑΙ 0
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
cap.release()
cv2.destroyAllWindows()
