from Trigonometria_Grados import sin,cos
import time
import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np


def TrayectoriaPersonalizada():
    plt.xlim([-2.5,2.5])
    plt.ylim([4.2,9.2])
    print("Ingresa los puntos de la figura que deseas que aprenda el robot."
          + "\n(Para terminar )")
    x = plt.ginput(n=-1, show_clicks = True)
    ruta = []
    for i in x:
        a = i[0]
        b = i[1]    
        ruta.append([a,b])
    print("Ruta:\n", ruta)
    plt.close()
    plt.show()
    return ruta

def Trayectoria_Lineal(Final):
    inicioT = Final[0]
    finalT = Final[-1]
    vec0 = np.round_(np.linspace(inicioT[0],finalT[0],10))
    vec1 = np.round_(np.linspace(inicioT[1],finalT[1],10))
    vec2 = np.round_(np.linspace(inicioT[2],finalT[2],10))
    vecReturn = []
    for i in range(10):
        vecReturn.append([int(vec0[i]),int(vec1[i]),int(vec2[i])])
    return vecReturn
    

def Ver_Trayectoria(Ang,Robot,Pts,vx,vy):
    plt.figure(figsize=(12,6))
    global R
    global Brazos
    global Angulos
    global Puntos
    global X
    global Y
    global VXF
    global VYF
    X = []
    Y = []
    VXF = vx
    VYF = vy
    Puntos = Pts
    Angulos = Ang
    Brazos  = [Robot.L1, Robot.L2, Robot.L3]
    for R in range(len(Angulos)):
        drawnow(draw_fig)
    time.sleep(2)
    plt.close()

def draw_fig():
    plt.subplot(1,2,1)
    a,b,c =Angulos[R]
    Bx1 = Brazos[0]*cos(a)
    Bx2 = Brazos[0]*cos(a)+ Brazos[1]*cos(a+b)
    Bx3 = Brazos[0]*cos(a)+ Brazos[1]*cos(a+b)+ Brazos[2]*cos(a+b+c)
    By1 = Brazos[0]*sin(a)
    By2 = Brazos[0]*sin(a)+ Brazos[1]*sin(a+b)
    By3 = Brazos[0]*sin(a)+ Brazos[1]*sin(a+b)+ Brazos[2]*sin(a+b+c)
    X.append(Bx3)
    Y.append(By3)
    plt.ylim(-1,11)
    plt.xlim(-6,6)
    plt.grid(True)
    plt.title("Cinemática inversa Robot Planar 3 Brazos")
    plt.plot([0,Bx1], [0,By1],'b')
    plt.plot([Bx1, Bx2], [By1, By2],'r')
    plt.plot([Bx2,Bx3], [By2,By3],'b')
    plt.plot(Bx3,By3,"*r")
    for i in Puntos:
        plt.plot(i[0],i[1],'*b')
    for i in range(len(VXF)):
        plt.plot(VXF[i],VYF[i],'r')
    plt.subplot(1,2,2)
    plt.ylim(-1,11)
    plt.xlim(-6,6)
    plt.grid(True)
    plt.title("Cinemática inversa Robot Planar 3 Brazos")
    for i in range(len(VXF)):
        plt.plot(VXF[i],VYF[i],'r')
    plt.plot(X,Y,'b')
