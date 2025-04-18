from typing import List
from datetime import datetime


def generate_stock_list_str(stocks: List[str]):
    stocks_with_quote = ["'" + stock + "'" for stock in stocks]
    stocks_list_string = ",".join(stocks_with_quote)
    return stocks_list_string


def generate_get_stock_price_sql_string(
    stocks: List[str], start_date: datetime, end_date: datetime
) -> str:
    stock_list_sql_format = generate_stock_list_str(stocks)
    sql_string = f"select date, close, ticker from stocks_price where ticker in ({stock_list_sql_format}) and date >= '{start_date}' and date<='{end_date}'"
    return sql_string


def generate_get_stock_sector_sql_string(
    stocks: List[str], start_date: datetime, end_date: datetime
) -> str:
    stock_list_sql_format = generate_stock_list_str(stocks)
    sql_string = f"select distinct s.ticker, sector from stocks_price as s join sp500_HOLDINGS as h on s.ticker = h.ticker  where s.ticker in ({stock_list_sql_format}) and date >= '{start_date}' and date<='{end_date}'"
    return sql_string
