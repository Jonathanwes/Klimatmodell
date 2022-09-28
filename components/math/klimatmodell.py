# -*- coding: utf-8 -*-

import numpy as np
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



        
    
    