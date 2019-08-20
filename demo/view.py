from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table

from .server import app
import os
import pandas as pd


view_layout = [
    html.Div(id="table_view", children=[
        dash_table.DataTable(id='table'),
    ]),

    html.Button("Show data.", id="show_data")
]


@app.callback(Output("table_view", "children"),
              [Input("show_data", "n_clicks")])
def show_data(n_clicks):
    for file in os.listdir():
        if file.endswith(".csv"):
            # Show only the first 15 rows and 7 columns
            df = pd.read_csv(file).iloc[:15, :7]

            return dash_table.DataTable(id="table",
                                        columns=[{"name": i, "id": i}
                                                 for i in df.columns],
                                        data=df.to_dict("rows"))

    return html.Div("Nothing to display.")
