from . import ids
from dash import Dash, dcc, html
from dash.dependencies import Input,Output
from .models import plots

def draw_klimatmodell(app: Dash,itterationer,resolution) -> html.Div:
    
    plottar=plots.create_1d_plots(itterationer,resolution)
    @app.callback(
        Output(ids.PLOTTAR, "children"),
        Input(ids.SLIDER1, "value")
        )
    def bars(itteration):
        return html.Div(children=[html.Div([
                                    html.Div([html.H3("Albedo "+str(itteration)),plottar[itteration][0]],className="col 6"),
                                    html.Div([html.H3("Temperatur "+ str(itteration)),plottar[itteration][1]],className="col 6")],className="row"),
                    html.Div([
                                      html.Div([plottar[itteration][2]],className="col 6"),
                                      html.Div([plottar[itteration][3]],className="col 6")
                                  ],className="row")
                    ])
    
    
    
    return html.Div( 
        children=[
            html.Div(
                id=ids.PLOTTAR,
            ),
            html.Div(
                dcc.Slider(
                    min=0,
                    max=itterationer,
                    value=0,
                    step=1,
                    id=ids.SLIDER1,
                    marks={i: i  for i in range(itterationer)}
                )
              )
            ]
        )
