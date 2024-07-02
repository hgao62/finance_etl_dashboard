import plotly.express as px
from utils import generate_get_stock_sector_sql_string
from db import read_from_sql

def generate_sector_pie_chart(stocks, start_date, end_date, first_load):
    if first_load:
        sql_string = generate_get_stock_sector_sql_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT distinct stock, sector FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
        stocks = ["AMZN"]
    data = read_from_sql(sql_string)
    piechart=px.pie(
            data_frame=data,
            names="sector",
            hole=.3,
            title= "Sector Distribution of Selected Stocks"
            )
    return piechart