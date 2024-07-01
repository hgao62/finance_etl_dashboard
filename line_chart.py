from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_mantine_components as dmc
import plotly.express as px
from db import read_from_sql
from dash_id import DashComponentID
data = px.data.stocks()

app = Dash(__name__)




def get_ticker_list():
    df = read_from_sql("select ticker_name from ticker_list")
    return list(df["ticker_name"])

TICKER_LIST = get_ticker_list()
LINE_CHART =dmc.SimpleGrid(
[
    dcc.Graph(id=DashComponentID.LINE_CHART),
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
