from . import ids
from dash import Dash, dcc, html
from dash.dependencies import Input,Output
from .models import plots

def draw_klimatmodell(app: Dash,itterationer,resolution) -> html.Div:
    #km,sphere_coords=create_model(itterationer,resolution) 
    
    #country_oulines=spherical_country_outlines.country_outlines(1.05)
    plottar=plots.create_1d_plots(itterationer,resolution)
    
    @app.callback(
        Output(ids.PLOTTAR, "children"),
        Input(ids.SLIDER1, "value")
        )
    def bars(itteration):
        return plottar[itteration]
    
    return html.Div( 
        children=[
            html.Div(
                id=ids.PLOTTAR,
            ),
            html.Div(
                dcc.Slider(
                    min=0,
                    max=itterationer,
                    value=1,
                    step=1,
                    id=ids.SLIDER1,
                    marks={i: i  for i in range(0,itterationer)}
                )
              )
            ]
        )
