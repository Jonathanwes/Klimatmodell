# -*- coding: utf-8 -*-

import numpy as np

class klimatmodell:
    def __init__(self):
        self.latitud=np.linspace(-np.pi/2,np.pi/2,50)
        self.steffe=5.67*10**(-8)
        self.start_albedo=start_albedo(self.latitud)
        
    def emissivitet(x):
        return 0.929789+0.000335482*np.degrees(x)-0.000179486*np.degrees(x)**2 - 7.16273 * 10**-7*np.degrees(x)**3 +9.40092*10**-8*np.degrees(x)**4 + 2.33581*10**-10*np.degrees(x)**5 -1.90827*10**-11*np.degrees(x)** 6 - 1.68775*10**-14*np.degrees(x)**7 +1.18909*10**-15*np.degrees(x)**8
    def S(x):
        return 1360*(1-0.48*((1/2)*(3*(np.sin(x)**2)-1)))
    def start_albedo(x):
        return 0.22255 + 0.000523706*np.degrees(x)+0.0000868482*np.degrees(x)**2-1.20516*10**-7*np.degrees(x)**3-3.68369*10**-9*np.degrees(x)**4
    
    def albedo(T: np.array) -> np.array:
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
    
    def calc_T(self,albedot): #räknar ut Temperaturen för alla latituder
        self.temperaturen_hela_jorden=(self.S(self.latitud) * (1-albedot) / (4*self.steffe*(1-(self.emissivitet (self.latitud)/2) )))**(1/4)
    



def klimatmodell():
    
    
    
    def albedo(T): #Räknar ut albedot för en temperatur. 
        Ai=0.7
        A0=0.289
        Ti=260
        T0=293
        if T<Ti:
            return Ai
        if Ti<T<T0:
            return A0 + (Ai-A0)*((T-T0)**2 / ((Ti-T0))**2)
        if T>T0:
            retu'rn A0
        
    def alla_albedo(temperatur): #räknar ut albedot för alla latituder
        albedolista=[]
        for i in range(len(temperatur)):
            albedolista.append(albedo(temperatur[i]))
        return albedolista
    
    def calc_T(albedot,en_latitud): #räknar ut Temperaturen för en latidud
        return (S(en_latitud)*(1-albedot)/(4*steffe*(1-(emissivitet(en_latitud)/2))))**(1/4)
    
    def alla_temperaturer(albedo30): #räknar ut temperaturen för alla latituder
        temperatur=[]
        for i in range(len(albedo30)):
            temperatur.append(calc_T(albedo30[i],latitud[i]))
        return temperatur
        
    def test(albedot_på_hela_jorden):
        integral=np.trapz(albedot_på_hela_jorden,latitud)
        #medel=sum(albedot_på_hela_jorden)/(len(albedot_på_hela_jorden))
        medel=((integral-0.7)/2)
        a=(0.7-medel)/2.25
        return (a,medel)
    
    
    temperatur_på_hela_jorden=alla_temperaturer(start_albedo)
    
    for i in range(itterationer):
        albedot_på_hela_jorden=alla_albedo(temperatur_på_hela_jorden)
        temperatur_på_hela_jorden=alla_temperaturer(albedot_på_hela_jorden)
        #temperatur_på_hela_jorden=np.convolve(temperatur_på_hela_jorden, np.ones(25)/25, mode="same")
    
        #plt.plot(latitud,albedot_på_hela_jorden)
        #plt.plot(latitud,temperatur_på_hela_jorden)



        
    
    