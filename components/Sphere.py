import plotly.express as px
import numpy as np
import pandas as pd
from dash import Dash, dcc, html
from . import ids

def mega_function(app: Dash,itterationer):
    
    #Albedot räknar ut albedot för en ny temperatur
    #Calc_T ska räkna ut temperaturen för en given emessivitet och albedo
    
    
    #Solarkonstant beroende av latitud
    S = lambda x : 1360*(1-0.48*((1/2)*(3*(np.sin(x)**2)-1))) 
    
    #Funktion för att räkna ut emissivitet beroende av latitud
    emissivitet= lambda x : 0.929789+0.000335482*np.degrees(x)-0.000179486*np.degrees(x)**2 - 7.16273 * 10**-7*np.degrees(x)**3 +9.40092*10**-8*np.degrees(x)**4 + 2.33581*10**-10*np.degrees(x)**5 -1.90827*10**-11*np.degrees(x)** 6 - 1.68775*10**-14*np.degrees(x)**7 +1.18909*10**-15*np.degrees(x)**8
    
    #Funktion för att räkna ut startalbedot
    start_albedo= lambda x: 0.22255 + 0.000523706*np.degrees(x)+0.0000868482*np.degrees(x)**2-1.20516*10**-7*np.degrees(x)**3-3.68369*10**-9*np.degrees(x)**4
    
    steffe=5.67*10**(-8)
    
    #array av grader från -90,90
    latitud=np.linspace(-np.pi/2,np.pi/2,50)
    
    #Räknar ut startalbedo
    start_albedo=start_albedo(latitud)
    
    
    
    
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
            return A0
        
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



        
    x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
    y = x.copy().T
    z = np.cos(x ** 2 + y ** 2)
    resolution=50
    phi = np.linspace(0, 2*np.pi, 2*resolution)
    theta = np.linspace(0, np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    
    
    r=1
    cx,cy,cz=0,0,0
    r_xy = r*np.sin(theta)
    x = cx + np.cos(phi) * r_xy
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)
    
    new_x=[]
    new_y=[]
    new_z=[]
    color=[]
    
    for x1,y1,z1 in zip(x,y,z):
        new_x.extend(x1)
        new_y.extend(y1)
        new_z.extend(z1)
        #color.extend(S(z1)) ger solarkonstant istället
        color.extend((abs(np.array(temperatur_på_hela_jorden)-1)))
    #fig=go.Figure(data=[go.Scatter3d(x=new_x,y=new_y,z=new_z,mode="markers",marker={"color":albedot_på_hela_jorden})])
    
    for row in range(1):
        new_x.extend([0.1*row-1 for i in range(len(temperatur_på_hela_jorden))])
        new_y.extend([1 for i in range(len(temperatur_på_hela_jorden))])
        #new_z.append([0 for i in range(len(temperatur_på_hal_jorden))])
        new_z.extend(z[0])
        #color.extend(S(z1)) ger solarkonstanten istället
        color.extend((abs(np.array(temperatur_på_hela_jorden)-1)))
    
    

    
    data=pd.DataFrame(data={"x":new_x,"y":new_y,"latitud":new_z,"Temperatur":color})
    fig=px.scatter_3d(data,x="x",y="y",z="latitud",color="Temperatur",color_continuous_scale="thermal",title="Tempetratur (K\u00B0)      "+(str(itterationer)) )
    #fig=go.Figure(data=[go.Scatter3d(x=x[0],y=y[0],z=z[0],mode="markers",marker={"color":albedot_på_hela_jorden})])
    
    # Lägg till slider som ändrar albedot / temperaturen
    
    if itterationer==0:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    if itterationer==1:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    if itterationer==5:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    
