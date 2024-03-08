import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('stock_prices.db')
cursor = conn.cursor()

def insert_stock_price(ticker, price, date):
    cursor.execute('''
    INSERT INTO stock_prices (ticker, price, date)
    VALUES (?, ?, ?)
    ''', (ticker, price, date))
    conn.commit()

# Example usage
insert_stock_price('AAPL', 150.10, '2024-03-09 10:00:00')
