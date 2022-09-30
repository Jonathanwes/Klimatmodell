from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout


def main() -> None:
    app=Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "3d-Plottar över 1-d modell, utan värmefördelning"
    app.layout= create_layout(app)
    app.run()
    
    
if __name__ == "__main__":
    main()
    
