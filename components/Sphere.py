import plotly.express as px
import numpy as np
import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go    

from . import ids
from mpl_toolkits.basemap import Basemap
import numpy as np

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
    

    
    

    def degree2radians(degree):
        #convert degrees to radians
        return degree*np.pi/180
    
    def mapping_map_to_sphere(lon, lat, radius=1):
        #this function maps the points of coords (lon, lat) to points onto the  sphere of radius radius
        
        lon=np.array(lon, dtype=np.float64)
        lat=np.array(lat, dtype=np.float64)
        lon=degree2radians(lon)
        lat=degree2radians(lat)
        xs=radius*np.cos(lon)*np.cos(lat)
        ys=radius*np.sin(lon)*np.cos(lat)
        zs=radius*np.sin(lat)
        return xs, ys, zs
    
    # Make shortcut to Basemap object, 
    # not specifying projection type for this example
    m = Basemap() 
    
    
    # Functions converting coastline/country polygons to lon/lat traces
    def polygons_to_traces(poly_paths, N_poly):
        ''' 
        pos arg 1. (poly_paths): paths to polygons
        pos arg 2. (N_poly): number of polygon to convert
        '''
        # init. plotting list
        lons=[]
        lats=[]
    
        for i_poly in range(N_poly):
            poly_path = poly_paths[i_poly]
            
            # get the Basemap coordinates of each segment
            coords_cc = np.array(
                [(vertex[0],vertex[1]) 
                 for (vertex,code) in poly_path.iter_segments(simplify=False)]
            )
            
            # convert coordinates to lon/lat by 'inverting' the Basemap projection
            lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
        
            
            lats.extend(lat_cc.tolist()+[None]) 
            lons.extend(lon_cc.tolist()+[None])
            
           
        return lons, lats
    
    # Function generating coastline lon/lat 
    def get_coastline_traces():
        poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
        N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
        cc_lons, cc_lats= polygons_to_traces(poly_paths, N_poly)
        return cc_lons, cc_lats
    
    # Function generating country lon/lat 
    def get_country_traces():
        poly_paths = m.drawcountries().get_paths() # country polygon paths
        N_poly = len(poly_paths)  # use all countries
        country_lons, country_lats= polygons_to_traces(poly_paths, N_poly)
        return country_lons, country_lats


    # Get list of of coastline, country, and state lon/lat 
    
    cc_lons, cc_lats=get_coastline_traces()
    country_lons, country_lats=get_country_traces()
    
    #concatenate the lon/lat for coastlines and country boundaries:
    lons=cc_lons+[None]+country_lons
    lats=cc_lats+[None]+country_lats
    
    new_x2=[]
    new_y2=[]
    new_z2=[]
    color2=[]
    for row in range(20):
        new_x2.extend([0.1*row-1 for i in range(len(temperatur_på_hela_jorden))])
        new_y2.extend([1.1 for i in range(len(temperatur_på_hela_jorden))])
        #new_z.append([0 for i in range(len(temperatur_på_hal_jorden))])
        new_z2.extend(z[0])
        #color.extend(S(z1)) ger solarkonstanten istället
        color2.extend((abs(np.array(temperatur_på_hela_jorden)-1)))    
    
    xs, ys, zs=mapping_map_to_sphere(lons, lats, radius=1.1)# here the radius is slightly greater than 1 
    #data2={"x":zs,"y":ys,"latitud":zs}
    #data1=pd.DataFrame(data={"x":new_x,"y":new_y,"latitud":new_z,"Temperatur":color})
    
    trace1=go.Scatter3d(x=xs,y=ys,z=zs,marker={"size":1,"color":"black"})
    trace2=go.Scatter3d(x=new_x,y=new_y,z=new_z,marker={"color":color,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    trace3=go.Scatter3d(x=new_x2,y=new_y2,z=new_z2,marker={"color":color2})
    
    layout={"title":"Temperatur efter " + str(itterationer)}
    
    fig=go.Figure(data=[trace1,trace2,trace3],layout=layout)
    # Lägg till slider som ändrar albedot / temperaturen
    
    if itterationer==0:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    if itterationer==1:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    if itterationer==5:
        return dcc.Graph(figure=fig,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    
