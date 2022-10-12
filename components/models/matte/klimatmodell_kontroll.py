# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 08:47:02 2022

@author: Jonat
"""

import numpy as np
class klimatmodell_start:
    """
    Definerar modellen och håller koll på modellens värden
    
    resolution är för hur många latituder modellen arbetar
    start_albedo är en funktion för att räkna ut albedot för att starta modellen
    
    """
    
    def __init__(self,resolution , start_albedo=lambda latitud :0.22255 + 0.000523706*np.degrees(latitud)+0.0000868482*np.degrees(latitud)**2-1.20516*10**-7*np.degrees(latitud)**3-3.68369*10**-9*np.degrees(latitud)**4):
        self.resolution=resolution # kan vara bra att ha när det sedan ska bli en sfär
        self.latitud=np.linspace(-np.pi/2,np.pi/2, self.resolution) #latituden används endast för att räkna ut startvärden för arrayen
        self.steffe=5.67*10**(-8)
        self.albedot_hela_jorden=start_albedo(self.latitud)
        self.solar_konstant=self.S(self.latitud)
        self.emissivitet_konstant=self.emissivitet(self.latitud)
        
        
        
    def emissivitet(self,latitud): #Räknar ut emissiviteten för varje latitud förändras inte under modellens gång
        return 0.46*(0.929789+0.000335482*np.degrees(latitud)-0.000179486*np.degrees(latitud)**2 - 7.16273 * 10**-7*np.degrees(latitud)**3 +9.40092*10**-8*np.degrees(latitud)**4 + 2.33581*10**-10*np.degrees(latitud)**5 -1.90827*10**-11*np.degrees(latitud)** 6 - 1.68775*10**-14*np.degrees(latitud)**7 +1.18909*10**-15*np.degrees(latitud)**8)
    
    def S(self,latitud):
        return 1360*(1-0.48*((1/2)*(3*(np.sin(latitud)**2)-1)))
    
    def albedo(self):
        if not hasattr(self , "temperaturen_hela_jorden"): # Could create a try/except but wont bother
            print("Run Calc_T first to create a temperature")
            return 
    
        T=self.temperaturen_hela_jorden
        Ai=0.7   #gör dessa värden förändringsbara?
        A0=0.289
        Ti=260
        T0=293
        
        
        albedot=np.zeros(T.shape)
        albedot[T<=Ti]=Ai
        albedot[T>=T0]=A0
        
        middle_indexes=np.logical_and(Ti<T,T<T0) # creates Boolean array, neater solution probably exists
        
        albedot[middle_indexes] = A0 + (Ai-A0)*((T[middle_indexes]-T0)**2 / ((Ti-T0))**2)
        self.albedot_hela_jorden=albedot
        #self.albedo_utjämning()
        return self.albedot_hela_jorden
    
    
    def calc_T(self): #räknar ut Temperaturen för alla latituder
        self.temperaturen_hela_jorden=(self.solar_konstant * (1-self.albedot_hela_jorden) / (4*self.steffe*(1-(self.emissivitet_konstant)/2)))**(1/4)
       # self.temperatur_utjämning()
        return self.temperaturen_hela_jorden
    
    def temperatur_utjämning(self):
        factor=0.6
        procent_70 = self.temperaturen_hela_jorden*factor
        medel_procent_70=sum(procent_70)/len(procent_70)*1.1
     #   print(medel_procent_70,"medel")
    #    print(self.temperaturen_hela_jorden[0], "innan")
        self.temperaturen_hela_jorden=self.temperaturen_hela_jorden*(1-factor)+medel_procent_70
   #     print(self.temperaturen_hela_jorden[0], "efter")
        
    def albedo_utjämning(self):
        factor=0
        procent_70 = self.albedot_hela_jorden*factor
        medel_procent_70=sum(procent_70)/len(procent_70)
  #      print(medel_procent_70,"medel")
 #       print(self.albedot_hela_jorden[25], "innan")
        self.albedot_hela_jorden=self.albedot_hela_jorden*(1-factor)+medel_procent_70
#        print(self.albedot_hela_jorden[25], "efter")

        
        


class klimatmodell_kontroll:
    """
    En klass för att styra modellen och som lagrar värdena för varje itteration
    
    argument
    skickar in en klimatmodell, gör det möjligt att sätta en ny startalbedo eller resolution
    """
    def __init__(self, klimatmodell=klimatmodell_start(50)):
        self.klimatmodell=klimatmodell
        self.itteration=0
        self.temperatur_itterationer=[]
        self.albedo_itterationer=[]
        self.albedo_itterationer.append(self.klimatmodell.albedot_hela_jorden)
        self.temperatur_itterationer.append(self.klimatmodell.calc_T())
        
    def itterera(self,steg):
        self.itteration+=steg
        for i in range(steg):
            self.albedo_itterationer.append(self.klimatmodell.albedo())
            self.temperatur_itterationer.append(self.klimatmodell.calc_T())


            
if __name__=="__main__":#Debug
    #import sfär
    import matplotlib.pyplot as plt
    a=klimatmodell_kontroll(klimatmodell=klimatmodell_start(200))
    a.itterera(30)
    plt.scatter(a.klimatmodell.latitud,a.albedo_itterationer[30])
    plt.xlabel("latitud")
    plt.ylabel("albedo")
    plt.title("Emissivitet ${\cdot}$ 0.46")
    #fig=plt.figure()
    #ax=fig.add_subplot(projection="3d")
    #x,y,z=sfär.sfär(100,1)
    
    #ax.scatter(x,y,z,c=[a.albedo_itterationer[0] for x in range(50)])
    

    
    