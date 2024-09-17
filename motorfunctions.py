import RPi.GPIO as GPIO#Το module

GPIO.setmode(GPIO.BOARD)#Αρίθμηση των φυσικών pin

speed=50
#Τα pins
V1=11
C1=13
D1=15
V2=29
C2=31
D2=33

#Δεξιά ρόδα
GPIO.setup(V1, GPIO.OUT)
GPIO.setup(C1, GPIO.OUT)
GPIO.setup(D1, GPIO.OUT)
pwm1=GPIO.PWM(V1,100)
pwm1.start(speed)

#Αριστερή ρόδα
GPIO.setup(V2, GPIO.OUT)
GPIO.setup(C2, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)
pwm1=GPIO.PWM(V2,100)
pwm1.start(speed)

#Κίνηση μπροστά
def move_forw():
    GPIO.output(C1, GPIO.HIGH)
    GPIO.output(D1, GPIO.LOW)

    GPIO.output(C2, GPIO.HIGH)
    GPIO.output(D2, GPIO.LOW)

    GPIO.output(V1, GPIO.HIGH)
    GPIO.output(V2, GPIO.HIGH)
    return None

#Αριστερή περιστροφή
def turn_left():
    GPIO.output(C1, GPIO.HIGH)
    GPIO.output(D1, GPIO.LOW)

    GPIO.output(C2, GPIO.LOW)
    GPIO.output(D2, GPIO.HIGH)

    GPIO.output(V1, GPIO.HIGH)
    GPIO.output(V2, GPIO.HIGH)
    return None

#Δεξιά περιστροφή
def turn_right():
    GPIO.output(C1, GPIO.LOW)
    GPIO.output(D1, GPIO.HIGH)

    GPIO.output(C2, GPIO.HIGH)
    GPIO.output(D2, GPIO.LOW)

    GPIO.output(V1, GPIO.HIGH)
    GPIO.output(V2, GPIO.HIGH)
    return None

#Σταμάτημα
def stop():
    
    GPIO.output(V1, GPIO.LOW)
    GPIO.output(V2, GPIO.LOW)
    return None

def clean():
    GPIO.cleanup()
    return None
