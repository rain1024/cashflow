import sqlite3
import pandas as pd
import plotly.graph_objects as go

class StockExchange:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_stock_prices(self, ticker, start_year, end_year):
        query = f"""
        SELECT date, price FROM stock_prices 
        WHERE ticker = '{ticker}' 
        AND date >= '{start_year}-01-01' 
        AND date <= '{end_year}-12-31'
        ORDER BY date ASC
        """
        df = pd.read_sql_query(query, self.conn)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df.resample('M').first()