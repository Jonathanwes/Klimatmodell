import OOPklimatmodell_där_kontrollen_inte_ärver as km
import sfär
from dash import Dash, dcc, html
import plotly.graph_objects as go    
import Sfär_med_länder_osv_verkar_fungera


#skapar klimatmodell och gör att det går att plotta den.

def create_model(itterationer=10,resolution=50) -> km.klimatmodell_kontroller:
    klimatmodell=km.klimatmodell_kontroll(klimatmodell=km.klimatmodell_start(resolution))
    klimatmodell.itterera(itterationer)
    sphere=sfär.sfär(resolution)
    return klimatmodell,sphere

def klimatmodell_grafik(klimatmodell :km.klimatmodell_kontroll, sphere, itteration=1): 
    
    outlines=Sfär_med_länder_osv_verkar_fungera.country_outlines(1.05)
    
    albedo_plott=go.Scatter3d(x=sphere[0],y=sphere[1],z=sphere[2],marker={"color":[klimatmodell.albedo_itterationer[itteration] for x in range(len(sphere[0]))] ,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    temperatur_plott=go.Scatter3d(x=sphere[0],y=sphere[1],z=sphere[2],marker={"color":[klimatmodell.temperatur_itterationer[itteration] for x in range(len(sphere[0]))] ,"colorbar":{"thickness":10,"x" : 0.9,"len":0.7}})
    
    return albedo_plott,temperatur_plott, outlines


def draw_klimatmodell(app: Dash,itterationer,resolution) -> html.Div:
    km,sphere=create_model(itterationer,resolution) #ska bara köras en gång
    albedo_plott,temperatur_plott,outlines=klimatmodell_grafik(km,sphere) 
    
    
    return html.Div(
        )
