from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from .upload import upload_layout
from .view import view_layout


app.layout = html.Div(children=[

    dcc.Tabs(id="tabs", value='upload_data', children=[
        dcc.Tab(label='Upload Data', value='upload_data',
                id="upload_data"),
        dcc.Tab(label='View Data', value='view_data',
                id="view_data"),
    ]),

    html.Div(id="content"),
])


@app.callback(Output('content', 'children'),
              [Input('tabs', 'value')])
def tab_subpages(tab):

    if tab == 'upload_data':
        return upload_layout

    else:
        return view_layout
