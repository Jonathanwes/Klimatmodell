from .matte import klimatmodell_kontroll as km
from .matte import sphere
from .matte import spherical_country_outlines
from . import ids
from dash import Dash, dcc, html
import plotly.graph_objects as go    
from dash.dependencies import Input,Output



#import matplotlib.pyplot as plt


#skapar klimatmodell och gör att det går att plotta den.

def create_model(itterationer=10,resolution=50) -> km.klimatmodell_kontroll:
    klimatmodell=km.klimatmodell_kontroll(klimatmodell=km.klimatmodell_start(resolution))
    klimatmodell.itterera(itterationer)
    sphere_coords=sphere.sfär(resolution)
    return klimatmodell,sphere_coords

def klimatmodell_grafik(klimatmodell :km.klimatmodell_kontroll, sphere_coords, outlines, itteration=1): 
    
    x,y,z=sphere_coords
    
    new_x,new_y,new_z=[],[],[]
    temperatur_color=[]
    albedo_color=[]
    
    for x1,y1,z1 in zip(x,y,z): #packar upp x,y,z
        new_x.extend(x1)
        new_y.extend(y1)
        new_z.extend(z1)
        #color.extend(S(z1)) ger solarkonstant istället
        temperatur_color.extend(klimatmodell.temperatur_itterationer[itteration])
        albedo_color.extend(klimatmodell.albedo_itterationer[itteration]) #color *50 istället?
    
    #temperatur_plott_2=go.Scatter3d(x=new_x,y=new_y,z=new_z,marker={"color":temperatur_color,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    #fig3=go.Figure(data=[temperatur_plott_2,outlines])

    
    albedo_plott=go.Scatter3d(x=new_x,y=new_y,z=new_z,marker={"color":albedo_color,"colorscale":"RdBu" ,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    layout1={"title":"Albedo efter " + str(itteration)+"itterationer"}
    fig1=go.Figure(data=[albedo_plott,outlines],layout=layout1)
    
    albedo_plott = dcc.Graph(figure=fig1,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    temperatur_plott=go.Scatter3d(x=new_x,y=new_y,z=new_z,marker={"color": temperatur_color,"colorscale": "solar" ,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})    
    layout2={"title":"Temperatur efter " + str(itteration)+ "itterationer"}
    fig2=go.Figure(data=[temperatur_plott,outlines],layout=layout2)
    temperatur_plott = dcc.Graph(figure=fig2,style={'display': 'inline-block','width': '70vh', 'height': '70vh'})
    return temperatur_plott,albedo_plott



def draw_klimatmodell(app: Dash,itterationer,resolution) -> html.Div:
    km,sphere_coords=create_model(itterationer,resolution) 
    
    country_oulines=spherical_country_outlines.country_outlines(1.05)

    @app.callback(
        Output(ids.PLOTTAR, "children"),
        Input(ids.SLIDER1, "value")
        )
    def bars(itteration):
        return klimatmodell_grafik(km,sphere_coords,country_oulines,itteration)
    
    return html.Div(
        children=[
            html.Div(
                id=ids.PLOTTAR,
            ),
            html.Div(
                dcc.Slider(
                    min=0,
                    max=10,
                    value=1,
                    step=1,
                    id=ids.SLIDER1,
                    marks={i: i  for i in range(10)}
                )
             )
            ]
        )
