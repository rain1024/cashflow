import click
import sqlite3
from datetime import datetime
import json
import plotly.graph_objects as go

# Function to initialize the database with the updated table schema
def init_db():
    # Connect to your SQLite database
    conn = sqlite3.connect('stocks.db')

    # Create a cursor object
    cur = conn.cursor()

    # SQL for creating the stock_prices table according to the new schema
    create_table_sql = ''' CREATE TABLE IF NOT EXISTS stock_prices (
                                        id INTEGER PRIMARY KEY,
                                        ticker TEXT NOT NULL,
                                        price REAL NOT NULL,
                                        date TIMESTAMP NOT NULL,
                                        UNIQUE(ticker, date)
                                    ); '''

    # Execute the create table SQL command
    cur.execute(create_table_sql)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    click.echo('Database initialized successfully with the stock_prices table.')

def import_data(filename):
    conn = sqlite3.connect('stocks.db')
    cur = conn.cursor()

    # Open and load the JSON file
    with open(filename) as f:
        data = json.load(f)

    for ticker, time_price_pairs in data.items():
        for pair in time_price_pairs:
            timestamp_ms, price = pair
            if timestamp_ms < 0:
                # print(f"Skipping record with out-of-range date for ticker {ticker}")
                continue
            # Convert timestamp from milliseconds to seconds for SQLite TIMESTAMP format
            timestamp = datetime.utcfromtimestamp(timestamp_ms / 1000)
            insert_sql = '''INSERT OR IGNORE INTO stock_prices (ticker, price, date) VALUES (?, ?, ?);'''
            cur.execute(insert_sql, (ticker, price, timestamp))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    click.echo(f'Data imported successfully from {filename}')

def viz_tickers(tickers):
    conn = sqlite3.connect('stocks.db')
    cur = conn.cursor()
    fig = go.Figure()

    for ticker in tickers:
        query_sql = '''SELECT date, price FROM stock_prices WHERE ticker = ? ORDER BY date'''
        cur.execute(query_sql, (ticker,))
        rows = cur.fetchall()
        if rows:
            dates = [row[0] for row in rows]
            prices = [row[1] for row in rows]
            fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name=ticker))
    
    fig.update_layout(title=f'Stock Prices Comparison',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.show()

@click.group()
def cli():
    pass

@cli.command('init')
def init_comand():
    """Initialize the database with the stock_prices table."""
    init_db()

@cli.command('import')
@click.argument('filename')
def import_command(filename):
    """Import data from a JSON file into the database."""
    import_data(filename)

@cli.command('viz')
@click.argument('tickers', nargs=-1)
def viz_command(tickers):
    """Visualize the price data for given tickers."""
    if not tickers:
        click.echo("Please provide at least one ticker.")
        return
    viz_tickers(tickers)


if __name__ == '__main__':
    cli()