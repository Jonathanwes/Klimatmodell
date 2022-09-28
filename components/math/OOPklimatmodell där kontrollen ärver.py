# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 08:47:02 2022

@author: Jonat
"""

class klimatmodell_start:
    def __init__(self):
        self.latitud=np.linspace(-np.pi/2,np.pi/2,50)
        self.steffe=5.67*10**(-8)
        self.albedot_hela_jorden=self.start_albedo(self.latitud)
        
    def emissivitet(self,x):
        return 0.929789+0.000335482*np.degrees(x)-0.000179486*np.degrees(x)**2 - 7.16273 * 10**-7*np.degrees(x)**3 +9.40092*10**-8*np.degrees(x)**4 + 2.33581*10**-10*np.degrees(x)**5 -1.90827*10**-11*np.degrees(x)** 6 - 1.68775*10**-14*np.degrees(x)**7 +1.18909*10**-15*np.degrees(x)**8
    def S(self,x):
        return 1360*(1-0.48*((1/2)*(3*(np.sin(x)**2)-1)))
    def start_albedo(self,x):
        return 0.22255 + 0.000523706*np.degrees(x)+0.0000868482*np.degrees(x)**2-1.20516*10**-7*np.degrees(x)**3-3.68369*10**-9*np.degrees(x)**4
    
    def albedo(self,T: np.array) -> np.array:
        Ai=0.7
        A0=0.289
        Ti=260
        T0=293
        albedot=np.zeros(T.shape)
        albedot[T<Ti]=Ai
        albedot[T>T0]=A0
        
        middle_indexes=np.logical_and(Ti<T,T<T0) # creates Boolean array, neater solution probably exists
        albedot[middle_indexes] = A0 + (Ai-A0)*((T[middle_indexes]-T0)**2 / ((Ti-T0))**2)
        self.albedot_hela_jorden=albedot
        return self.albedot_hela_jorden
    
    def calc_T(self,albedot): #räknar ut Temperaturen för alla latituder
        self.temperaturen_hela_jorden=(self.S(self.latitud) * (1-albedot) / (4*self.steffe*(1-(self.emissivitet (self.latitud)/2) )))**(1/4)
        return self.temperaturen_hela_jorden


class klimatmodell_kontroll(klimatmodell_start):
    def __init__(self):
        
        klimatmodell_start.__init__(self)
        
        self.itteration=0
        self.temperatur_itteration=[]
        self.albedo_itterationer=[]
        self.albedo_itterationer.append(self.albedot_hela_jorden)
        self.temperatur_itteration.append(self.calc_T(self.albedot_hela_jorden))
        
    def itterera(self,steg):
        self.itteration+=steg
        for i in range(steg):
            self.albedo_itterationer=self.albedo(self.temperaturen_hela_jorden)
            self.temperatur_itteration.append(self.calc_T(self.albedot_hela_jorden))
            
if __name__=="__main__":#Debug
    import numpy as np
    a=klimatmodell_kontroll()
    print(a.temperatur_itteration)
    a.itterera(5)
    
    