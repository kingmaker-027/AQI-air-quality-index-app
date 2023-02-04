# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
from pages import sample1, sample2, sample3, sample4 , sample5, final
from components import navbar


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nav = navbar.Navbar()
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname =='/':
        return sample1.layout
    if pathname == '/sample1':
        return sample1.layout
    if pathname == '/sample2':
        return sample2.layout
    if pathname == '/sample3':
        return sample3.layout
    if pathname == '/sample4':
        return sample4.layout
    if pathname == '/sample5':
        return sample5.layout 
    if pathname == '/final':
        return final.layout       
    else:
        return "404 Page Error! Please choose a link"

if __name__ == '__main__':
    app.run_server()
    # app.run_server(debug=True)
