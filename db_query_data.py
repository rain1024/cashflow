import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('stock_prices.db')
cursor = conn.cursor()

def get_stock_prices(ticker):
    cursor.execute('''
    SELECT * FROM stock_prices WHERE ticker = ?
    ''', (ticker,))
    return cursor.fetchall()

# Example usage
print(get_stock_prices('AAPL'))