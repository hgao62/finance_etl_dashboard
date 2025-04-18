import plotly.express as px
from utils import generate_get_stock_sector_sql_string
from db import read_from_sql


def generate_sector_pie_chart(stocks, start_date, end_date, first_load):
    if first_load:
        sql_string = generate_get_stock_sector_sql_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT distinct s.ticker, sector from stocks_price as s join sp500_HOLDINGS as h on s.ticker = h.ticker where s.ticker= 'AMZN' and date >= '2024-01-01'"
        stocks = ["AMZN"]
    data = read_from_sql(sql_string)
    piechart = px.pie(
        data_frame=data,
        names="Sector",
        hole=0.3,
        title="Sector Distribution of Selected Stocks",
    )

    piechart.update_layout(
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
    )
    return piechart
