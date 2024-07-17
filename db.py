from sqlalchemy import create_engine
import sqlalchemy

import pandas as pd

MYSQL_CONNECTION_STRING = (
    "mysql+mysqlconnector://airflow_user:airflow_pass@localhost/airflow_db"
)
MYSQL_ENGINE = create_engine(MYSQL_CONNECTION_STRING)


def read_from_sql(sql_query: str) -> pd.DataFrame:
    with MYSQL_ENGINE.connect() as conn:
        res = pd.read_sql(sql_query, conn)
        print(res.head())
        return res


if __name__ == "__main__":
    sql = "select * from stock_history"
    read_from_sql(sql)
