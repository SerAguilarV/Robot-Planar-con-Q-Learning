import time
import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np
from Trigonometria_Grados import sin,cos

def CrearObstaculosCirculo(Puntos):

    repetirFig = int(input("\n\n¿Cuántos obstaculos habrá? : " ))
    plt.xlim([-2.5,2.5])
    plt.ylim([4.2,9.2])
    VXF = []
    VYF = []
    centro=[]
    radios = []
    for i in range(repetirFig):
        vecX = []
        vecY = []
        plt.xlim([-2.5,2.5])
        plt.ylim([4.2,9.2])
        print("Da click en el centro del Circulo " +
              "y en donde estara la circunferencia")
        for i in Puntos:
            plt.plot(i[0],i[1],'*b')
        objeto = plt.ginput(n=2, show_clicks = True)
        plt.close()
        plt.show()
        centro.append(objeto[0])
        radio = np.sqrt((objeto[0][0]-objeto[1][0])**2 + (objeto[0][1]-objeto[1][1])**2)
        radios.append([radio])
        for i in range(0,360,int(360/90)):
            X = radio * cos(i) + objeto[0][0]
            Y = radio * sin(i) + objeto[0][1]
            vecX.append(X)
            vecY.append(Y)
        vecX.append(vecX[0])
        vecY.append(vecY[0])
        VXF.append(vecX)
        VYF.append(vecY)
    
    PlotearObstaculo(VXF,VYF,Puntos)
    return VXF,VYF , centro , radios  # poner Vector de Radio y Centros

def CrearObstaculosRectangulo(Puntos):

    repetirFig = int(input("\n\n¿Cuántos obstaculos habrá? : " ))
    plt.xlim([-2.5,2.5])
    plt.ylim([4.2,9.2])
    VXF = []
    VYF = []
    limites=[]
    for i in range(repetirFig):
        vecY = []
        vecX =[]
        plt.xlim([-2.5,2.5])
        plt.ylim([4.2,9.2])
        print("\nDa click en la superior izquierda del rectangulo\n" +
              "y en donde estara la inferior derecha")
        for i in Puntos:
            plt.plot(i[0],i[1],'*b')
        objeto = plt.ginput(n=2, show_clicks = True)
        limites.append([objeto[0][0], objeto[0][1], objeto[1][0], objeto[1][1]])
        v1 = list(np.linspace(objeto[0][1],objeto[1][1],10))
        h1 = list(np.linspace(objeto[0][0],objeto[1][0],10))
        v2 = v1.copy()
        v2.reverse()
        h2 = h1.copy()
        h2.reverse()
        vecY = list(np.ones(10)*objeto[0][1]) + v1 + list(np.ones(10)*objeto[1][1]) + v2
        vecX = h1 + list(np.ones(10)*objeto[0][0]) + h2 + list(np.ones(10)*objeto[1][0])
        VXF.append(vecX)
        VYF.append(vecY)
    PlotearObstaculo(VXF,VYF,Puntos)
    return VXF,VYF,limites

def PlotearObstaculo(VXF,VYF,Puntos):
    for i in Puntos:
        plt.plot(i[0],i[1],'*b')    
    for i in range(len(VXF)):
        plt.plot(VXF[i],VYF[i],'r')
        plt.xlim([-2.5,2.5])
        plt.ylim([4.2,9.2])
    plt.show()


##if __name__ == '__main__':
##    print("Crear Obstaculo tipo rectangulo")
##    VXF,VYF,limites = CrearObstaculosRectangulo()
##    print("\n")
##    print(VXF,VYF,limites)
##    print("Crear Obstaculo tipo circulo")
##    VXF,VYF , centro , radios = CrearObstaculosCirculo()
##    print("\n")
##    print(VXF,VYF , centro , radios)
