import sqlite3

import pandas as pd
import requests
from config import settings



class AlphaVantageAPI:
    def __init__(self, api_key=settings.alpha_api_key):
        self.__api_key = api_key
    
    def get_daily(self, ticker, output_size="full"):
        
        # Create URL
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY&"
            f"symbol={ticker}&"
            f"outputsize={output_size}&"
            "datatype=json&"
            f"apikey={self.__api_key}"
            )
        
        # Send HTTP request using Python
        response = requests.get(url)
        response_data = response.json()
        
        # Raise Exception for incorrect ticker
        if "Time Series (Daily)" not in response_data.keys():
            raise Exception(
                f"Invalid API call. Check {ticker} is correct"
                )
        
        # Convert from JSON to dataframe + clean
        data = response_data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(data, orient="index", dtype=float)
        
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        
        df.columns = [col.split(". ")[1] for col in df.columns]
        
        return df

class SQLRepo:
    def __init__(self, connection):
        # Assign connection to SQL Repo
        self.connection = connection
        
    def insert_table(self, table_name, records, if_exists="fail"):
        
        n_inserted = records.to_sql(
            name=table_name,
            con=self.connection,
            if_exists=if_exists
        )
        
        return n_inserted
    
    
    def read_table(self, table_name, limit=None):
        
        # Create SQL Query
        if limit:
            sql = f"SELECT * FROM '{table_name}' LIMIT {limit}"
        else:
            sql = f"SELECT * FROM '{table_name}'"
        
        # Read query into df
        df = pd.read_sql(
            sql=sql, con=self.connection, parse_dates=["date"], index_col="date"
            )
        
        return df
        