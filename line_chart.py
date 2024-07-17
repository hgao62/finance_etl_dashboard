from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_mantine_components as dmc
import plotly.express as px
from db import read_from_sql
from dash_id import DashComponentID
from typing import List
from datetime import datetime
from utils import generate_stock_list_str, generate_get_stock_price_sql_string
import pandas as pd
import plotly.graph_objects as go
import dash_ag_grid as dag

data = px.data.stocks()

app = Dash(__name__)

STOCK_PRICE_DATA = read_from_sql(
    "SELECT date,close,stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
)
STOCK_VOLUME_DATA = read_from_sql(
    "SELECT date,volume, stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
)
STOCK_PRICE_TABLE_FIELD = [{"field": "date"}, {"field": "close"}, {"field": "stock"}]
STOCK_VOLUME_TABLE_FIELD = [{"field": "date"}, {"field": "volume"}, {"field": "stock"}]


def convert_to_time_series_format(data: pd.DataFrame) -> pd.DataFrame:
    df = data.pivot_table("close", ["date"], "stock")
    df = df.reset_index(0).reset_index(drop=True)
    return df


def get_stock_price_data(sql_string):
    stock_data = read_from_sql(sql_string)
    stock_data_time_series_format = convert_to_time_series_format(stock_data)
    return stock_data_time_series_format


def generate_stock_line_chart_and_underlying_data(
    stocks, start_date, end_date, first_load
):
    if first_load:
        sql_string = generate_get_stock_price_sql_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT date,close,stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
        stocks = ["AMZN"]
    # stock_data_time_series_format = get_stock_price_data(sql_string)
    stock_data = read_from_sql(sql_string)
    stock_data_time_series_format = convert_to_time_series_format(stock_data)
    stock_line_chart = px.line(
        data_frame=stock_data_time_series_format,
        x="date",
        y=stocks,
        template="seaborn",
        title="Stock Price Over Time",
    )
    stock_line_chart.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        yaxis_title="Price",
        xaxis_title="Date",
        legend_title="Stock",
    )
    return stock_line_chart, stock_data


def generate_stock_volume_string(stocks, start_date, end_date):
    stock_list_sql_format = generate_stock_list_str(stocks)
    sql_string = f"select date,volume, stock from airflow_db.stock_history where stock in ({stock_list_sql_format}) and date >= '{start_date}' and date<='{end_date}'"
    return sql_string


def generate_stock_volume_line_chart_and_underlying_data(
    stocks, start_date, end_date, first_load
):
    if first_load:
        sql_string = generate_stock_volume_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT date,volume, stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
        stocks = ["AMZN"]
    stock_volumes_data = read_from_sql(sql_string)
    return (
        px.line(
            stock_volumes_data.sort_values(by=["date"], ascending=[True]),
            x="date",
            y="volume",
            color="stock",
            facet_col="stock",
            title="Volume Traded Over Time",
        ),
        stock_volumes_data,
    )


def get_ticker_list():
    df = read_from_sql("select ticker_name from ticker_list")
    return list(df["ticker_name"])


STOCK_PRICE_TABLE_COLUMNS = {}
STOCK_VOLUME_TABLE_COLUMNS = {}

TICKER_LIST = get_ticker_list()
LINE_CHART = dmc.SimpleGrid(
    children=[
        dcc.Graph(id=DashComponentID.PRICE_CHART),
        dcc.Graph(id=DashComponentID.VOLUME_CHART),
        # html.Button("Download CSV", id="csv-button", n_clicks=0),
        dmc.Button(
            "Download Table Data",
            id=DashComponentID.PRICE_TABLE_DOWNLOAD_BUTTON,
            n_clicks=0,
        ),
        dag.AgGrid(
            id=DashComponentID.PRICE_TABLE,
            columnSize="sizeToFit",
            columnDefs=STOCK_PRICE_TABLE_FIELD,
            rowData=STOCK_PRICE_DATA.to_dict("records"),
            csvExportParams={
                "fileName": "price_table.csv",
            },
            dashGridOptions={"pagination": True, "grid-page-size": 10},
        ),
        dmc.Button(
            "Download Table Data",
            id=DashComponentID.VOLUME_TABLE_DOWNLOAD_BUTTON,
            n_clicks=0,
        ),
        dag.AgGrid(
            id=DashComponentID.VOLUME_TABLE,
            columnSize="sizeToFit",
            columnDefs=STOCK_VOLUME_TABLE_FIELD,
            rowData=STOCK_PRICE_DATA.to_dict("records"),
            csvExportParams={
                "fileName": "volume_table.csv",
            },
            dashGridOptions={"pagination": True, "grid-page-size": 10},
        ),
        dcc.Graph(id=DashComponentID.CUM_RETURN_CHART),
        dcc.Graph(id=DashComponentID.SECTOR_PIE_CHART)
        # dash_table.DataTable(
        #     data.to_dict("records"),
        #     [{"name": i, "id": i} for i in data.columns],
        #     page_size=10,
        #     style_table={"overflow-x": "auto"},
        # ),
    ],
    cols=2,
    id="simple_grid_layout",
    breakpoints=[
        {"maxWidth": 1500, "cols": 2, "spacing": "md"},
        {
            "maxWidth": 992,
            "cols": 1,
            "spacing": "sm",
        },  # common screen size for small laptops
        {
            "maxWidth": 768,
            "cols": 1,
            "spacing": "sm",
        },  # common screen size for tablets
    ],
)
# ,id = DashComponentID.ALL_CHARTS
# )
