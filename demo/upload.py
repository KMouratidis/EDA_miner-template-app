from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

from .server import app

import base64
import io
import os
import pandas as pd


upload_layout = [
    html.A(dcc.Upload(
        id='upload_data_button',
        children=html.Div('Drag and Drop or Select Files'),
        multiple=True,
    )),

    html.Div(id='output-data-upload'),
]


# Inspired by the Dash docs
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload_data_button', 'contents')],
              [State('upload_data_button', 'filename'),
               State('upload_data_button', 'last_modified')])
def parse_uploads(list_of_contents, list_of_names,
                  list_of_dates):

    if list_of_contents is not None:
        response = [parse_contents(c, n, d) for c, n, d
                    in zip(list_of_contents, list_of_names, list_of_dates)]

        return response

    else:
        raise PreventUpdate


# Taken straight out the Dash Docs.
def parse_contents(contents, filename, date):

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    name, extension = os.path.splitext(filename)

    try:
        if extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df.to_csv(filename)
            return html.Div("Data uploaded successfully.")

        else:
            return html.Div('Format not yet supported.')

    except:
        return html.Div('There was an error processing this file.')

