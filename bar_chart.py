import plotly.graph_objects as go
from db import read_from_sql
from utils import generate_stock_list_str, generate_get_stock_price_sql_string
import pandas as pd



def calculate_cumulative_return(stock_history):
    """
    Function to enrich the stock history data.

    Arguments:
        stock_history: Pandas DataFrame with historical stock data.

    Return:
        Enriched Pandas DataFrame.
    """
    # Perform data enrichment operations here
    # For example, calculate daily returns
    stock_history["daily_return"] = stock_history["close"].pct_change()
    stock_history["cumulative_return"] = (1 + stock_history["daily_return"]).cumprod()
    return stock_history

def get_top_three_cum_return_stocks(stocks_return):
    """Get top three stocks return up until the latest date available in the data"""
    cum_returns = pd.pivot_table(stocks_return, columns=["stock"], index=["date"])

        # compute cumulative returns pct change
    daily_pct_change = cum_returns.pct_change()
    daily_pct_change.fillna(0, inplace=True)
    cumprod_daily_pct_change = (1 + daily_pct_change).cumprod()

    cumprod_daily_pct_change.columns = [
        "_".join([str(index) for index in multi_index])
        for multi_index in cumprod_daily_pct_change.columns.ravel()
    ]
    cumprod_daily_pct_change = cumprod_daily_pct_change.reset_index()
    max_date = cumprod_daily_pct_change['date'].max()
    latest_cumprod_change = cumprod_daily_pct_change[cumprod_daily_pct_change["date"] == max_date]
    latest_cumprod_change = latest_cumprod_change.melt(id_vars =["date"], var_name="stock", value_name = "cum_return")
    # rows to column https://stackoverflow.com/questions/28654047/convert-columns-into-rows-with-pandas
    latest_cumprod_change = latest_cumprod_change.round(4)
    latest_cumprod_change = latest_cumprod_change.sort_values(by=["cum_return"], ascending=False)
    top_three_stocks= latest_cumprod_change.head(3)# select top 3 rows
    
    latest_cumprod_change_worst = latest_cumprod_change.sort_values(by=["cum_return"])
    bottom_three_stocks= latest_cumprod_change_worst.head(3)# select top 3 rows
    final_result = pd.concat([top_three_stocks, bottom_three_stocks])
    return top_three_stocks

def generate_top_three_return_bar_charts(stocks, start_date, end_date, first_load):
    if first_load:
     sql_string = generate_get_stock_price_sql_string(stocks, start_date, end_date)
    else:
        sql_string = "SELECT date,close,stock FROM airflow_db.stock_history where stock= 'AMZN' and date >= '2024-01-01'"
        stocks = ["AMZN"]
    price_data = read_from_sql(sql_string)
    # price_data_with_cum_return = calculate_cumulative_return(price_data)
    top_three_stocks_return = get_top_three_cum_return_stocks(price_data)
    x_axis_data = top_three_stocks_return["cum_return"].to_list()
    y_axis_data = top_three_stocks_return["stock"].to_list()
    fig = go.Figure( go.Bar(
    x=x_axis_data ,
    y=y_axis_data,
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),
    name='Top 3 cumulative return stocks',
    orientation='h',
))
    fig.update_layout(
    title='Top 3 cumulative return stocks',
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.5],
    ),
    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)
    fig.update_layout(xaxis = dict(tickmode ='linear', tick0 = 0, dtick = 0.3))
    # format tick https://plotly.com/python/tick-formatting/
    annotations = []
    for  xd, yd in zip(x_axis_data,y_axis_data):

        annotations.append(dict(xref='x1', yref='y1',
                                y=yd, x=xd +0.3,
                                text=str(xd) ,
                                font=dict(family='Arial', size=12,
                                        color='rgb(50, 171, 96)'),
                                showarrow=False))
    fig.update_layout(annotations=annotations)

    return fig
   