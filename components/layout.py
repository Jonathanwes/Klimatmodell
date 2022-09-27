from dash import Dash, html
from . import Sphere

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.P("ska lägga till mer sen, en slider för itterationer och en glob för varje variabel vi vill undersöka"),
            html.Div(
                children=[
                    html.Div(
                    children=[Sphere.mega_function(app,0),Sphere.mega_function(app,1),Sphere.mega_function(app,5)]),
            ]
            )

            ],
            
    )
    
    