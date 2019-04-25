import numpy as np
import sys
import math
from Trigonometria_Grados import sin,cos

Add = 5
Saltos = 5
Regla = 19
Acciones_Vec = [[Add,0,0],[-Add,0,0],[0,Add,0],[0,-Add,0],[0,0,Add],[0,0,-Add]]

class Robot:
    def __init__(self,L1=4,L2=3,L3=3,numeroPuntos = 0,Alpha = 0.8,Gamma = 0.8):
        self.Q = np.zeros([numeroPuntos-1,Regla**3,6])/100
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.X = 0
        self.Y = 0
        self.XFinal=0
        self.YFinal=0
        self.Alpha = Alpha
        self.Gamma = Gamma
        self.Angulos=np.zeros(3,dtype = np.int)
        self.Angulos_Ant=np.zeros(3,dtype = np.int)
        self.Reco=0
        self.Maximo=0
        self.d=0
        self.Accion = 0
        self.S = 0
        self.S_1 = 0
        self.crash = False
        self.distPoint = 0
        self.find = False
        self.It = 0
        self.Accion2 = 0
        self.tramo = 0

    def Elegir_Accion(self):
        S = int(self.Calcular_Estado())
        self.S = S
        maxim=max(self.Q[self.tramo][S][:])
        flag=0
        a=0
        indice_max=0
        for i in self.Q[self.tramo][S][:]:
            if i == maxim:
                flag+=1
                indice_max=a
            if flag>1:
                break
            a+=1
        if flag != 1:
            x = self.Accion_Random(S,maxim)
            self.Accion = x
        else:
            self.Accion = indice_max
        return     

    def Calcular_Estado(self):
        return int((self.Angulos_Ant[0]/Saltos)+(self.Angulos_Ant[1]/Saltos)*Regla +(self.Angulos_Ant[2]/Saltos)*(Regla**2))
        
    def Accion_Random(self,S,maxim):
        Indices = []
        for i in range(len(self.Q[self.tramo][S][:])):
            if self.Q[self.tramo][S][i] == maxim:
                Indices.append(i)
        Random = np.random.randint(0,len(Indices))
        return Indices[Random]

    def Ejecutar_Accion(self):
        for i in range(3):
            self.Angulos[i] = self.Angulos[i] + Acciones_Vec[self.Accion][i]
            if self.Angulos[i]>85 or self.Angulos[i]<5 :
                self.crash = True
        
    def Obtener_Estado_Siguiente(self):
        self.S_1 = self.Calcular_Estado2()
        
    def Calcular_Estado2(self):
        return int((self.Angulos[0]/Saltos)+(self.Angulos[1]/Saltos)*Regla +(self.Angulos[2]/Saltos)*(Regla**2))
        
    def Elegir_Accion_Siguiente(self):
        St1 = self.S_1
        maxim=max(self.Q[self.tramo][St1][:])
        flag=0
        a=0
        indice_max=0
        for i in self.Q[self.tramo][St1][:]:
            if i == maxim:
                flag+=1
                indice_max=a
            if flag>1:
                break
            a+=1
        if flag != 1:
            x = self.Accion_Random(St1,maxim)
            self.Accion2 = x
        else:
            self.Accion2 = indice_max
        return     
    
    def Recompensa(self,crearObst,limites):
        A1,A2,A3 = self.Angulos
        self.X =(self.L1 * cos(A1) + (self.L2 * cos(A1+A2)) + (self.L3 * cos(A1+A2+A3)))
        self.Y =(self.L1 * sin(A1) + (self.L2 * sin(A1+A2)) + (self.L3 * sin(A1+A2+A3)))
        self.d=math.sqrt((self.XFinal-self.X)**2 + (self.YFinal-self.Y)**2)

        if crearObst == 1:
            for rec in limites:
                if rec[2]>=self.X>=rec[0] and rec[3]<=self.Y<=rec[1]:
                    self.crash = True
                    print("Muerto")
        elif crearObst == 2:
            for i in range(len(limites[0])):
                rad = limites[1][i]
                centro = limites[0][i]
                ec = np.sqrt((self.X-centro[0])**2 + (self.Y-centro[1])**2)                
                if ec<rad:
                    self.crash = True
            
        if self.d <= 0.2:
            self.find = True
            
        if self.d>=self.distPoint or self.crash == True:
            self.Reco = -1
        elif self.d>=0.2:
            self.Reco = 0
        else:
            self.Reco = 1
            self.find = True
    
    def Actualizar_Q_QLearning(self):
        S = self.S
        a = self.Accion
        r = self.Reco
        Greddy = max(self.Q[self.tramo][self.S_1][:])
# =============================================================================
#         Val = np.zeros(1,dtype = np.float64)
# =============================================================================
# =============================================================================
#         Val = self.Q[self.tramo][S][a].copy()
# =============================================================================
        self.Q[self.tramo][S][a] = (1-self.Alpha) * self.Q[self.tramo][S][a] + self.Alpha*(r+self.Gamma*Greddy)
# =============================================================================
#         if Val == self.Q[self.tramo][S][a]:
#             print('Murio')
#             print(self.S)
#             print(self.S_1)
#             print(self.It)
#             sys.exit()
# =============================================================================
        #if self.It%5000==0:
            #self.Q=self.Q+np.ones([Regla**3,6])/20
        self.Angulos_Ant = self.Angulos.copy()
        self.It += 1
        
    def Actualizar_Q_Sarsa(self):
        S = self.S
        a = self.Accion
        r = self.Reco
        Greddy = self.Q[self.tramo][self.S_1][self.Accion2]
# =============================================================================
#         Val = np.zeros(1,dtype = np.float64)
# =============================================================================
# =============================================================================
#         Val = self.Q[self.tramo][S][a].copy()
# =============================================================================
        self.Q[self.tramo][S][a] = self.Q[self.tramo][S][a]+self.Alpha*(r+self.Gamma*Greddy - self.Q[self.tramo][S][a])
# =============================================================================
#         if Val == self.Q[self.tramo][S][a]:
#             print('Murio')
#             print(self.S)
#             print(self.S_1)
#             print(self.It)
#             sys.exit()
# =============================================================================
        #if self.It%5000==0:
            #self.Q=self.Q+np.ones([Regla**3,6])/20
        A,B,C = self.Angulos
        self.Angulos_Ant = [A,B,C]
        A2 = self.Accion2
        self.Accion = A2
        self.It += 1
        
    def Actualizar_Q_Backward(self):
        S = self.S
        a = self.Accion
        r = self.Reco
        Greddy = self.Q[self.tramo][self.S_1][self.Accion2]
# =============================================================================
#         Val = np.zeros(1,dtype = np.float64)
#         Val = self.Q[self.tramo][S][a].copy()
# =============================================================================
        self.Q[self.tramo][S][a] = self.Q[self.tramo][S][a]+self.Alpha*(r+self.Gamma*Greddy - self.Q[self.tramo][S][a])
# =============================================================================
#         if Val == self.Q[self.tramo][S][a]:
#             print('Murio')
#             print(self.S)
#             print(self.S_1)
#             print(self.It)
#             sys.exit()
# =============================================================================
        A,B,C = self.Angulos
        self.Angulos_Ant = [A,B,C]
        A2 = self.Accion2
        self.Accion = A2
        self.It += 1
        s = S
        s2 = self.S_1
        if s == s2:
            sys.exit()
        return s, a, r, s2

    def Busqueda(self,pInicial):
        d = 1
        while d>=0.2:
            a = np.random.randint(0,100)
            b = np.random.randint(0,100)
            c = np.random.randint(0,100)
            Bx3 = self.L1*cos(a)+ self.L2*cos(a+b)+ self.L3*cos(a+b+c)
            By3 = self.L1*sin(a)+ self.L2*sin(a+b)+ self.L3*sin(a+b+c)
            d = np.sqrt( (Bx3-pInicial[0])**2 + (By3-pInicial[1])**2 )
        return a,b,c
