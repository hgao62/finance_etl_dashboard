import dash_mantine_components as dmc
from dash import Dash, dcc, html, Input, Output, dash_table, callback, State
import dash_bootstrap_components as dbc
from db import read_from_sql
from line_chart import (
    LINE_CHART,
    generate_stock_line_chart_and_underlying_data,
    generate_stock_volume_line_chart_and_underlying_data,
)
from bar_chart import generate_top_three_return_bar_charts
from pie_chart import generate_sector_pie_chart
from heading import HEADER
from dash_id import DashComponentID
import plotly.express as px
from typing import List
from datetime import datetime
import pandas as pd

# The line `import dash_ag_grid as dag` is importing the `dash_ag_grid` library and aliasing it as
# `dag`. This allows you to refer to the library using the shorter alias `dag` throughout your code
# instead of typing out the full library name `dash_ag_grid`. This can make your code more concise and
# easier to read.
import dash_ag_grid as dag

app = Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)


def get_ticker_list():
    df = read_from_sql("select distinct stock from airflow_db.stock_history")
    return list(df["stock"])


TICKER_LIST = get_ticker_list()


app.layout = html.Div(
    [
        dmc.Title("Stocks Analytics", align="center"),
        dmc.Space(h=20),
        # dmc.Button("Download Table Data", id="btn_csv"),
        # dcc.Download(id="download-dataframe-csv"),
        dmc.Space(h=10),
        dmc.MultiSelect(
            label="Select stock you like!",
            placeholder="Select all stocks you like!",
            id=DashComponentID.STOCK_DROP_DOWN,
            value=["AMZN"],
            data=[{"label": i, "value": i} for i in TICKER_LIST],
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.DatePickerRange(
                        id=DashComponentID.DATE_PICKER,
                        start_date=datetime(2024, 1, 1).date(),
                        end_date=datetime(2024, 6, 1).date(),
                        min_date_allowed=datetime(2019, 12, 1).date(),
                        max_date_allowed=datetime.today().date(),
                        initial_visible_month=datetime(2024, 1, 1).date(),
                    ),
                    width=2,
                ),
                dbc.Col(
                    dmc.Button(
                        id=DashComponentID.RUN_BTN,
                        children="Run",
                        n_clicks=0,
                        size = "md"
                        # variant="outline",
                    ),
                    width={"size":4}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        dmc.Container(
            [dmc.Space(h=60), LINE_CHART],
            fluid=True,
        ),
    ]
)


@callback(
    Output(DashComponentID.PRICE_CHART, "figure"),
    Output(DashComponentID.VOLUME_CHART, "figure"),
    Output(DashComponentID.CUM_RETURN_CHART, "figure"),
    Output(DashComponentID.SECTOR_PIE_CHART, "figure"),
    Output(DashComponentID.PRICE_TABLE, "rowData"),
    Output(DashComponentID.VOLUME_TABLE, "rowData"),
    State(DashComponentID.DATE_PICKER, "start_date"),
    State(DashComponentID.DATE_PICKER, "end_date"),
    State(DashComponentID.STOCK_DROP_DOWN, "value"),
    Input(DashComponentID.RUN_BTN, "n_clicks"),
)
def plot_line_chart(start_date, end_date, stocks: List[str], n_clicks):
    (
        stock_price_line_chart,
        stock_price_data,
    ) = generate_stock_line_chart_and_underlying_data(
        stocks, start_date, end_date, n_clicks
    )
    (
        stock_volume_line_chart,
        stock_volume_data,
    ) = generate_stock_volume_line_chart_and_underlying_data(
        stocks, start_date, end_date, n_clicks
    )
    stock_cum_return_chart = generate_top_three_return_bar_charts(
        stocks, start_date, end_date, n_clicks
    )

    stock_sector_pie_chart = generate_sector_pie_chart(
        stocks, start_date, end_date, n_clicks
    )

    return (
        stock_price_line_chart,
        stock_volume_line_chart,
        stock_cum_return_chart,
        stock_sector_pie_chart,
        stock_price_data.to_dict("records"),
        stock_volume_data.to_dict("records"),
    )


@callback(
    Output(DashComponentID.PRICE_TABLE, "exportDataAsCsv"),
    Input(DashComponentID.PRICE_TABLE_DOWNLOAD_BUTTON, "n_clicks"),
)
def export_price_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False


@callback(
    Output(DashComponentID.VOLUME_TABLE, "exportDataAsCsv"),
    Input(DashComponentID.VOLUME_TABLE_DOWNLOAD_BUTTON, "n_clicks"),
)
def export_volume_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False


if __name__ == "__main__":
    app.run_server(port=2409)
