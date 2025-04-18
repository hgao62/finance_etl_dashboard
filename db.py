from sqlalchemy import create_engine
import sqlalchemy

import pandas as pd

MYSQL_CONNECTION_STRING = (
    "mysql+mysqlconnector://airflow_user:airflow_pass@localhost/airflow_db"
)
MYSQL_ENGINE = create_engine(MYSQL_CONNECTION_STRING)
SQLITE_DB_PATH = r"C:\development\repo\finance_etl_dashboard\stock_analytics.db"
SQLITE_CONNECTION_STRING = f"sqlite:///{SQLITE_DB_PATH}"
SQLITE_ENGINE = create_engine(SQLITE_CONNECTION_STRING)

def read_from_sql(sql_query: str, engine = SQLITE_ENGINE) -> pd.DataFrame:
    with engine.connect() as conn:
        res = pd.read_sql(sql_query, conn)
        print(res.head())
        return res


if __name__ == "__main__":
    sql = "select * from stock_price"
    read_from_sql(sql)
