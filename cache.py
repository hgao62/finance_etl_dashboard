from db import read_from_sql

class Cache:
    _instance = None
    def __init__(self):
        if not hasattr(self,"ticker_list"):
            self.ticker_list  =[]
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(cls)
        return cls._instance
    
    def get_ticker_list(self):
        if not self.ticker_list:
            df = read_from_sql("select distinct stock from airflow_db.stock_history")
            self.ticker_list = list(df["stock"])
        return self.ticker_list
    


cache_instance = Cache()
TICKER_LIST = cache_instance.get_ticker_list()

