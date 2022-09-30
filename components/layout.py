from dash import Dash, html
#from . import Sphere
from . import klimatmodell_sfär_grafik_html as klimatmodell

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            klimatmodell.draw_klimatmodell(app, 10,50)
            ],

            
            
    )
    
    