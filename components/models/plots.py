# -*- coding: utf-8 -*-

#from . import create_models
from . import create_models as cm
import plotly.graph_objects as go    
from dash import dcc

def create_1d_plots(itterationer,resolution) -> dcc.Graph: 
    klimatmodell=cm.create_1d_model(resolution,itterationer)
    sphere,country_outlines=cm.create_sphere(resolution)
    x,y,z=sphere
    
    country_outlines=go.Scatter3d(x=country_outlines[0],y=country_outlines[1],z=country_outlines[2],marker={"size":1,"color":"black"})
    

    plots=[]
    for i in range(itterationer):
        print(i)
        albedo_color=[]
        temperature_color=[]
        
        for långdituder in range(len(x)):
            albedo_color.extend(klimatmodell.albedo_itterationer[i])
            temperature_color.extend(klimatmodell.temperatur_itterationer[i])    
            
        
        albedo_plott=go.Scatter3d(x=x , y=y , z=z , marker=
                                  {"color": albedo_color,
                                   "colorscale":"RdBu" ,
                                   "colorbar":{"thickness":10,"x" : 0.9,"len":0.7}
                                   })
        temperature_plott=go.Scatter3d(x=x,y=y, z=z, marker=
                                  {"color": temperature_color,
                                   "colorscale":"solar" ,
                                   "colorbar":{"thickness":10,"x" : 0.9,"len":0.7}
                                   })
        
        fig1=go.Figure(data=[albedo_plott,country_outlines])
        fig2=go.Figure(data=[temperature_plott,country_outlines])
        plots.append((dcc.Graph(figure=fig1)  ,  dcc.Graph(figure=fig2)))
    
    return plots