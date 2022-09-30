from dash import Dash, dcc, html
from . import ids
from dash.dependencies import Input,Output

def create_slider(app: Dash) -> html.Div:
    @app.callback(
        Output("text1", "children"),
        Input(ids.SLIDER1, "value")
        )
    def update_output(value):
        return value
    
    return html.Div(
        children=[
            dcc.Slider(
                min=1,
                max=10,
                value=1,
                step=1,
                id=ids.SLIDER1,
                marks={i: i  for i in range(10)}
            )
        ]
        )
        