import numpy as np
from Robot3GDL import Robot
from Trayectoria import Ver_Trayectoria, Trayectoria_Lineal, TrayectoriaPersonalizada
import sys
from Obstaculos import CrearObstaculosCirculo, CrearObstaculosRectangulo
#import Servos

if __name__ == '__main__':
    print("\n\n¿Qué tipo de trayectoria desea que tome el Robot?")
    tipoDeTrayectoria = int(input(" 1 - Trayectoria Predeterminada\n 2 - Trayectoria Personalizada\n\n"))
    if tipoDeTrayectoria == 1:
        Puntos = [[2,8.7], [0,8.7], [-2,8.7], [-2.2, 7.7], [-2,6.7], [0,6.7], [2,6.7], [2.2,5.7], [2,4.7], [0,4.7], [-2,4.7]]
        Robot_Planar = Robot(L1 = 4, L2 = 3, L3 = 3, numeroPuntos = len(Puntos))
        Ai,Bi,Ci = [40,50,20]
    else:
        Puntos = TrayectoriaPersonalizada()
        Robot_Planar = Robot(L1 = 4, L2 = 3, L3 = 3, numeroPuntos = len(Puntos))
        Ai,Bi,Ci = Robot_Planar.Busqueda(Puntos[0])
    #Puntos = [[2,8.7],  [-2,8.7], [-2,6.7],  [2,6.7], [2,4.7], [-2,4.7]]

    crearObst = int(input("¿Quieres crear obstaculos?, : \n 1 - Tipo Rectangulo "+
                    "\n 2 - Tipo Circular" + "\n 3 - Ninguno \nR: "))
    
    if crearObst == 1:
        VXF,VYF,limites = CrearObstaculosRectangulo(Puntos)
    elif crearObst == 2:
        VXF,VYF , centro , radios = CrearObstaculosCirculo(Puntos)
        limites = [centro,radios]
    else:
        print("\nSin obstaculos\n")
        VXF = []
        VYF = []        
    
    matrizTrayectoria = []
    trayectoriaLineal = []
    Iteraciones=0
    It=0
    It2 =0
    Num = 1
    BQSA = []
    Algoritmo = 0
    count = 0
    finalAnterior = []

    while Algoritmo<1 and Algoritmo<3:
        Algoritmo = int(input('\nIngresa que algoritmo quieres utilizar:\n  1- Q-Learning'
                      + '\n  2- Sarsa\n  3- Backward Q-Learning\n \n'))
        if Algoritmo<1 and Algoritmo<3:
            print('\n\n Algoritmo no identificado, porfavor seleccione una opcion\n\n')
            
    while True:

        Robot_Planar.Angulos_Ant = [Ai,Bi,Ci]
        Robot_Planar.Angulos = [Ai,Bi,Ci]
        Final = []
        Final.append([Ai,Bi,Ci])
        P=0
        
        while True:

            Robot_Planar.XFinal ,Robot_Planar.YFinal = Puntos[Robot_Planar.tramo+1]
            Robot_Planar.distPoint =np.sqrt( (Puntos[Robot_Planar.tramo][0]-Robot_Planar.XFinal)**2 + (Puntos[Robot_Planar.tramo][1]-Robot_Planar.YFinal)**2)

            while Robot_Planar.find == False and Robot_Planar.crash == False:

                Robot_Planar.Elegir_Accion()
                Robot_Planar.Ejecutar_Accion()
                Robot_Planar.Obtener_Estado_Siguiente()
                
                if Algoritmo == 2 or Algoritmo == 3:
                    Robot_Planar.Elegir_Accion_Siguiente()

                Robot_Planar.Recompensa(crearObst,limites)
                
                if Algoritmo == 1:
                    Robot_Planar.Actualizar_Q_QLearning()
                elif Algoritmo == 2:
                    Robot_Planar.Actualizar_Q_Sarsa()
                elif Algoritmo == 3:
                    s,a,r,s1 = Robot_Planar.Actualizar_Q_Backward()
                    BQSA.append([s,a,r,s1])
                
                A,B,C= Robot_Planar.Angulos
                Final.append([A,B,C])
                
            if Algoritmo == 3:
                for i in range(len(BQSA)):
                    s1,a1,r1,s2 = BQSA[-i]
                    Greddy = max(Robot_Planar.Q[Robot_Planar.tramo][s2][:])
                    Robot_Planar.Q[Robot_Planar.tramo][s1][a1] = (1-Robot_Planar.Alpha)*Robot_Planar.Q[Robot_Planar.tramo][s1][a1] +  Robot_Planar.Gamma*(r1+Robot_Planar.Gamma*Greddy)
                BQSA = []
            
            if Robot_Planar.find == True:
                Robot_Planar.find = False
            
            if Robot_Planar.crash == True:
                Robot_Planar.crash = False
                Final=[]
                break

            Iteraciones+=1

            if Final == finalAnterior:
                It2+=1
            else:
                finalAnterior = Final.copy()
                It2 = 0
                
            if It2 >= 10:
                print('{} puntos Conectados'.format(Robot_Planar.tramo+1))
                Ver_Trayectoria(Final, Robot_Planar, Puntos,VXF,VYF)
                if Num == 1:
                    trayectoriaLineal = Trayectoria_Lineal(Final)
                else:
                    temp = Trayectoria_Lineal(Final)
                    trayectoriaLineal = np.concatenate((trayectoriaLineal,temp)) 
                #for element in Final:
                    #Servos(element)
                P=0
            if It2 == 10:
                Num=Num+1
                Robot_Planar.tramo += 1
                Ai,Bi,Ci = Final[-1]
                print(Final)
                count+=len(Final)
                matrizTrayectoria.append(Final.copy())
                It2 = 0
                if Num == len(Puntos):
                    print("\n\nTrayectoria Trazada")
                    Final = []
                    for T in matrizTrayectoria:
                        for element in T:
                            Final.append(element)
                    print(Final)
                    Ver_Trayectoria(Final, Robot_Planar, Puntos,VXF,VYF)
                    print('\nNumero de Iteraciones: {}'.format(Robot_Planar.It))
                    #for i in Final:
                    #    Servos(i)
                    if not(crearObst == 1 or crearObst == 2):
                        print("Trayectoria Lineal")
                        Ver_Trayectoria(trayectoriaLineal, Robot_Planar, Puntos,VXF,VYF)
                    
                    input('Press enter to exit...')
                    sys.exit()
            else:
                break
