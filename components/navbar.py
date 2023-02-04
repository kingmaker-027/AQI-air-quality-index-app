# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("AQI", href="/sample1")),
                dbc.NavItem(dbc.NavLink("Pollutants", href="/sample2")),
                dbc.NavItem(dbc.NavLink("AQI Category", href="/sample3")),
                dbc.NavItem(dbc.NavLink("Avg Pollutants", href="/sample4")),
                dbc.NavItem(dbc.NavLink("AQI Level ", href="/sample5")),
                dbc.NavItem(dbc.NavLink("Future", href="/final")),

            ] ,
            brand="Indian AIR Quality App",
            brand_href="/sample1",
            color="dark",
            dark=True,
        ), 
    ])

    return layout