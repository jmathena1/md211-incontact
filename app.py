import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Div import Div
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import os
from datetime import datetime as d
from time import strftime
from pandas.core.reshape.merge import merge
import plotly.express as px
import plotly.graph_objects as go
import itertools
from dash.dependencies import Output, Input

#read in the data
calls_by_center_IR = pd.read_csv("calls_by_center_IR.csv")
calls_by_center_press1 = pd.read_csv("calls_by_center_press1.csv")

calls_by_hour_IR = pd.read_csv("calls_by_hour_IR.csv")
calls_by_hour_press1 = pd.read_csv("calls_by_hour_press1.csv")

repeat_calls_count_IR = pd.read_csv("repeat_calls_count_IR.csv")
repeat_calls_count_press1 = pd.read_csv("repeat_calls_count_press1.csv")

repeat_calls_count_range_IR = pd.read_csv("repeat_calls_range_count_IR.csv")
repeat_calls_count_range_press1 = pd.read_csv("repeat_calls_range_count_press1.csv")

#create month variable to store month names and sort order
d = {'Month': ['July', 'August', 'September', 'October', 'November', 'December', 'January'], 'Sort Order': [1, 2, 3, 4, 5, 6, 7]}
months_order = pd.DataFrame(data=d).sort_values(by="Sort Order")

##build app
#specify style sheet for use
external_stylesheets = [
    {
        "rel": "stylesheet"
    }
]

#create an instance of dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#create title of app
app.title = "211 Call Center Data Dashboard - inContact"
#create layout of app
app.layout = html.Div(
    children=[
        html.Div(
            children = [
            html.Img(src=app.get_asset_url("211-logo-1line-rgb.png"), className='header-logo'),
            html.H1(children='211 inContact KPI Dashboard', 
            className='header-title'),
                html.P(
                    children='Compare key peformance indicators on 211 Maryland partner call centers using inContact IVR data.',
                    className="sub-header"
                ),
            ],
            className='header',
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Select Month:", className="menu-title"),
                        dcc.Dropdown(
                            id="month",
                            options=[
                                {"label": month, "value": month}
                                for month in months_order.Month
                            ],
                            value="January",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className='menu',
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Tabs([
                            dcc.Tab(label = 'Press 1', children = [
                                dcc.Graph(
                                    id='calls_by_hour_press1',
                                    config={"displayModeBar": False},
                                    className="graph-text"
                                ),
                                dcc.Graph(
                                    id='calls_by_center_press1',
                                    config={"displayModeBar": False},
                                    className="graph-text"
                                ),
                                dcc.Graph(
                                    id='repeat_calls_count_press1',
                                    config={"displayModeBar": False},
                                    className="graph-text"
                                ),
                                dcc.Graph(
                                    id='repeat_calls_count_range_press1',
                                    config={"displayModeBar": False},
                                    className="graph-text"
                                )
                            ],
                            className="tab-title"
                        ),
                        dcc.Tab(label = 'Information and Referral (I & R)', children = [
                            dcc.Graph(
                                id='calls_by_hour_IR',
                                config={"displayModeBar": False},
                                className="graph-text"
                            ),
                            dcc.Graph(
                                id='calls_by_center_IR',
                                config={"displayModeBar": False},
                                className="graph-text"
                            ),
                            dcc.Graph(
                                id='repeat_calls_count_IR',
                                config={"displayModeBar": False},
                                className="graph-text"
                            ),
                            dcc.Graph(
                                id='repeat_calls_count_range_IR',
                                config={"displayModeBar": False},
                                className="graph-text"
                            )
                        ],
                        className="tab-title"
                    ),
                ]),
            ],
            className="card",
        ),
    ],
    className="wrapper",
),
],
)


##define callback functions
#define what value to track and what graphs to change
@app.callback(
    [Output("calls_by_hour_press1", "figure"), Output("calls_by_center_press1", "figure"), 
    Output("repeat_calls_count_press1", "figure"), Output("repeat_calls_count_range_press1", "figure"),
    Output("calls_by_hour_IR", "figure"), Output("calls_by_center_IR", "figure"), 
    Output("repeat_calls_count_IR", "figure"), Output("repeat_calls_count_range_IR", "figure")],
    [
        Input("month", "value"),
    ],
)
#definte update function
def update_charts(month):

    #create filtered datasets
    mask_hour_IR = ((calls_by_hour_IR.Month == month))
    mask_hour_press1 = ((calls_by_hour_press1.Month == month))
    calls_by_hour_IR_filtered = calls_by_hour_IR.loc[mask_hour_IR, :]
    calls_by_hour_press1_filtered = calls_by_hour_press1.loc[mask_hour_press1, :]

    mask_center_IR = ((calls_by_center_IR.Month == month))
    mask_center_press1 = ((calls_by_center_press1.Month == month))
    calls_by_center_IR_filtered = calls_by_center_IR.loc[mask_center_IR, :]
    calls_by_center_press1_filtered = calls_by_center_press1.loc[mask_center_press1, :]

    mask_calls_count_IR = ((repeat_calls_count_IR.Month == month))
    mask_calls_count_press1 = ((repeat_calls_count_press1.Month == month))
    repeat_calls_count_IR_filtered = repeat_calls_count_IR.loc[mask_calls_count_IR, :]
    repeat_calls_count_press1_filtered = repeat_calls_count_press1.loc[mask_calls_count_press1, :]

    mask_calls_count_range_IR = ((repeat_calls_count_range_IR.Month == month))
    mask_calls_count_range_press1 = ((repeat_calls_count_range_press1.Month == month))
    repeat_calls_count_range_IR_filtered = repeat_calls_count_range_IR.loc[mask_calls_count_range_IR, :]
    repeat_calls_count_range_press1_filtered = repeat_calls_count_range_press1.loc[mask_calls_count_range_press1, :]

    #create graphs - Press 1
    calls_by_hour_press1_figure = {
        "data": [
                    {
                        "x": calls_by_hour_press1_filtered["hour_of_day"],
                        "y": calls_by_hour_press1_filtered["Outbound"],
                        "type": "bar",
                        "marker": {"color": "#005191"},
                    },
                ],
        "layout": {
            "title": "Call Volume by Hour (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    calls_by_center_press1_figure = {
        "data": [
                    {
                        "x": calls_by_center_press1_filtered["Center"],
                        "y": calls_by_center_press1_filtered["Outbound"],
                        "type": "bar",
                        "marker": {"color": "#539ED0"},
                    },
        ],
        "layout": {
            "title": "Call Volume by Call Center (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    repeat_calls_count_press1_figure = {
        "data": [
                    {
                        "labels": repeat_calls_count_press1_filtered["Call Frequency"],
                        "values": repeat_calls_count_press1_filtered["# of Calls"],
                        "type": "pie",
                        "marker": {"colors": ["#005191", "#539ED0"]},
                    },
        ],
        "layout": {
            "title": "Repeat Callers vs One Time Callers (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    repeat_calls_count_range_press1_figure = {
        "data": [
                    {
                        "x": repeat_calls_count_range_press1_filtered["Call Count Range"],
                        "y": repeat_calls_count_range_press1_filtered["# of Calls"],
                        "type": "bar",
                        "marker": {"color": "#FF443B"},
                    },
        ],
        "layout": {
            "title": "Number of Calls Made by Repeat Callers (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    #create graphs - IR
    calls_by_hour_IR_figure = {
        "data": [
                    {
                        "x": calls_by_hour_IR_filtered["hour_of_day"],
                        "y": calls_by_hour_IR_filtered["Outbound"],
                        "type": "bar",
                        "marker": {"color": "#005191"},
                    },
        ],
        "layout": {
            "title": "Call Volume by Hour (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    calls_by_center_IR_figure = {
        "data": [
                    {
                        "x": calls_by_center_IR_filtered["Center"],
                        "y": calls_by_center_IR_filtered["Outbound"],
                        "type": "bar",
                        "marker": {"color": "#539ED0"},
                    },
        ],
        "layout": {
            "title": "Call Volume by Call Center (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    repeat_calls_count_IR_figure = {
        "data": [
                    {
                        "labels": repeat_calls_count_IR_filtered["Call Frequency"],
                        "values": repeat_calls_count_IR_filtered["# of Calls"],
                        "type": "pie",
                        "marker": {"colors": ["#005191", "#539ED0"]},
                    },
        ],
        "layout": {
            "title": "Repeat Callers vs One Time Callers (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }

    repeat_calls_count_range_IR_figure = {
        "data": [
                    {
                        "x": repeat_calls_count_range_IR_filtered["Call Count Range"],
                        "y": repeat_calls_count_range_IR_filtered["# of Calls"],
                        "type": "bar",
                        "marker": {"color": "#FF443B"},
                    },
                ],
        "layout": {
            "title": "Number of Calls Made by Repeat Callers (IVR)",
            "font": {"family":"Garamond", "size":14}
        },
    }
    return calls_by_hour_press1_figure, calls_by_center_press1_figure, repeat_calls_count_press1_figure, repeat_calls_count_range_press1_figure, calls_by_hour_IR_figure, calls_by_center_IR_figure, repeat_calls_count_IR_figure, repeat_calls_count_range_IR_figure


##run the app
if __name__ == "__main__":
    app.run_server(debug=True)
    