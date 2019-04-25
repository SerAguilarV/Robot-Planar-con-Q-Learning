import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
 

def servos(ang):
    GPIO.setmode(GPIO.BCM)   #Ponemos la Raspberry en modo BOARD

    GPIO.setup(21,GPIO.OUT)    #Ponemos el pin 21 como salida
    GPIO.setup(20,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)

    s1 = GPIO.PWM(21,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
    s2 = GPIO.PWM(20,50) 
    s3 = GPIO.PWM(16,50)

    s1.start(11.7)               #Enviamos un pulso del 7.5% para centrar el servo
    s2.start(11)
    s3.start(12.5)
  
    ang0 = 11.7 - round((ang[0]*0.1)/2.2,1);
    ang1 = 11 - round((ang[1]*0.1)/2,1);
    ang2 = 12.5 - round((ang[2]*0.1)/2.3,1);
 
    s1.ChangeDutyCycle(ang0)    #Enviamos un pulso del 4.5% para girar el servo hacia la izquierda
    time.sleep(0.2)           #pausa de medio segundo
    s2.ChangeDutyCycle(ang1)   #Enviamos un pulso del 10.5% para girar el servo hacia la derecha
    time.sleep(0.2)           #pausa de medio segundo
    s3.ChangeDutyCycle(ang2)    #Enviamos un pulso del 7.5% para centrar el servo de nuevo
    time.sleep(0.2)           #pausa de medio segundo
