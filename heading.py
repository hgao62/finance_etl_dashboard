import dash_mantine_components as dmc
from dash import Dash, dcc, html
import dash_core_components as dcc
from db import read_from_sql
from datetime import datetime
from dash_id import DashComponentID
from cache import TICKER_LIST

HEADER = html.Div(
    [
        dmc.Title("Equity prices - Line chart and Table data", align="center"),
        dmc.Space(h=20),
        dmc.Button("Download Table Data", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        dmc.Space(h=10),
        dmc.MultiSelect(
            label="Select stock you like!",
            placeholder="Select all stocks you like!",
            id=DashComponentID.STOCK_DROP_DOWN,
            value=["GOOG", "AAPL"],
            data=[{"label": i, "value": i} for i in TICKER_LIST],
        ),
        dcc.DatePickerRange(
            id=DashComponentID.DATE_PICKER,
            start_date=datetime(2014, 1, 1),
            end_date=datetime(2014, 1, 15),
            min_date_allowed=datetime(2014, 1, 1),
            max_date_allowed=datetime(2014, 12, 31),
            initial_visible_month=datetime(2014, 1, 1),
        ),
        html.Div(
            id="run-btn-outer",
            children=html.Button(
                id=DashComponentID.RUN_BTN, children="Run", n_clicks=0
            ),
        ),
    ]
)
