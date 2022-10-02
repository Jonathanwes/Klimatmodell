# -*- coding: utf-8 -*-

#from . import create_models
from . import create_models as cm
import plotly.graph_objects as go    
from dash import dcc

def create_1d_plots(resolution,itterationer):
    klimatmodell=cm.create_1d_model(50,10)
    sphere,country_outlines=cm.create_sphere(50)
    
    country_outlines=go.Scatter3d(x=country_outlines[0],y=country_outlines[1],z=country_outlines[2],marker={"size":1,"color":"black"})
    
    albedo_plott=go.Scatter3d(x=[i for i in sphere[0]] , y=[i for i in sphere[1]] , z=[i for i in sphere[2]]),#marker={"color":(klimatmodell.albedo_itterationer[0]),"colorscale":"RdBu" ,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    
    fig1=go.Figure(data=[albedo_plott,country_outlines])
    
    return dcc.Graph(figure=fig1)