
import dash_mantine_components as dmc
from dash import Dash, dcc, html, Input, Output, dash_table, callback,State
import dash_bootstrap_components as dbc
from db import read_from_sql
from line_chart import LINE_CHART
from heading import HEADER
from dash_id import DashComponentID
import plotly.express as px
from typing import List
from datetime import datetime
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])


def get_ticker_list():
    df = read_from_sql("select ticker_name from ticker_list")
    return list(df["ticker_name"])

TICKER_LIST = get_ticker_list()


app.layout = html.Div(
    [    dmc.Title(
        "Equity prices Analytics", align="center"),
    dmc.Space(h=20),
    dmc.Button("Download Table Data", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv"),
    dmc.Space(h=10),
    dmc.MultiSelect(
        label="Select stock you like!",
        placeholder="Select all stocks you like!",
        id=DashComponentID.STOCK_DROP_DOWN,
        value=['AMZN'],
        data=[{"label": i, "value": i} for i in TICKER_LIST],
    ),
    html.Br(),
    dbc.Row([dbc.Col(dcc.DatePickerRange(
                id=DashComponentID.DATE_PICKER,
                start_date=datetime(2024, 1, 1).date(),
                end_date=datetime(2024, 6,1).date(),
                min_date_allowed=datetime(2019, 12, 1).date(),
                max_date_allowed=datetime.today().date(),
                initial_visible_month=datetime(2024, 1, 1).date(),
    ),width=2),
    dbc.Col(dmc.Button(id=DashComponentID.RUN_BTN, children="Run", n_clicks=0, variant="outline"),width=3)
    ])
    ,
    html.Br(),
    html.Br(),
     dmc.Container(
    [
        dmc.Space(h=60),
        LINE_CHART
    ],
    fluid=True,
)]
)

def generate_get_stock_sql_string(stocks: List[str],start_date:datetime, end_date:datetime) ->str:
    
    def _generate_stock_list_str(stocks:List[str]):
        stocks_with_quote = ["'" + stock + "'" for stock in stocks ]
        stocks_list_string = ",".join(stocks_with_quote)
        return stocks_list_string
    stock_list_sql_format = _generate_stock_list_str(stocks)
    
    sql_string = f"select date, close, stock from airflow_db.stock_history where stock in ({stock_list_sql_format}) and date >= '{start_date}' and date<='{end_date}'"
    return sql_string

def convert_to_time_series_format(data:pd.DataFrame) -> pd.DataFrame:
    df = data.pivot_table("close",["date"],"stock")
    df = df.reset_index(0).reset_index(drop=True)
    return df
    

@callback(
    Output(DashComponentID.LINE_CHART, "figure"),
    State(DashComponentID.DATE_PICKER, "start_date"),
    State(DashComponentID.DATE_PICKER, "end_date"),
    State(DashComponentID.STOCK_DROP_DOWN, "value"),
    Input(DashComponentID.RUN_BTN, "n_clicks"),
  
)
def select_stocks(start_date, end_date, stocks:List[str],n_clicks):
    if n_clicks:
        sql_string = generate_get_stock_sql_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT date,close,stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
        stocks= ['AMZN']
    stock_data = read_from_sql(sql_string)
    stock_data_time_series_format = convert_to_time_series_format(stock_data)
    fig = px.line(data_frame=stock_data_time_series_format, x="date", y=stocks, template="simple_white")
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25), yaxis_title="Price", xaxis_title="Date"
    )
    return fig


# @callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(data.to_csv, "mydf.csv")


if __name__ == "__main__":
    app.run_server(port = 2409)