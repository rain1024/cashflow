import sqlite3
import pandas as pd
import plotly.graph_objects as go

def dca_final_performance_visualized(ticker, start_year=2010, end_year=2018, monthly_investment=20000000):
    # Connect to the database
    conn = sqlite3.connect('stocks.db')
    
    # Prepare the query to fetch monthly stock prices
    query = f"""
    SELECT date, price FROM stock_prices 
    WHERE ticker = '{ticker}' 
    AND date >= '{start_year}-01-01' 
    AND date <= '{end_year}-12-31'
    ORDER BY date ASC
    """
    
    # Fetch data and convert to DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Ensure data is monthly and set date as index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.resample('M').first()
    
    # Calculate total shares bought and total investment over the period
    df['shares_bought'] = monthly_investment / df['price']
    df['total_shares'] = df['shares_bought'].cumsum()
    df['monthly_investment'] = monthly_investment
    df['cumulative_investment'] = df['monthly_investment'].cumsum()
    
    df['year'] = df.index.year
    yearly_data = df.resample('Y').last()  # Resampling to get year-end values

    # Calculating yearly investment and shares held
    yearly_data['annual_investment'] = df['monthly_investment'].resample('Y').sum()
    yearly_data['annual_shares_held'] = yearly_data['total_shares']
    
    # Calculate performance percentage
    yearly_data['performance_percentage'] = ((yearly_data['price'] * yearly_data['total_shares'] - yearly_data['cumulative_investment']) / yearly_data['cumulative_investment']) * 100
    
    # Creating lists to store yearly data for visualization
    years = yearly_data.index.year.tolist()
    end_of_year_shares = yearly_data['total_shares'].tolist()
    end_of_year_values = (yearly_data['total_shares'] * yearly_data['price']).tolist()
    end_of_year_investments = yearly_data['cumulative_investment'].tolist()
    annual_investment = yearly_data['annual_investment'].tolist()
    annual_shares_held = yearly_data['annual_shares_held'].tolist()
    performance_percentage = yearly_data['performance_percentage'].tolist()

    # Visualization with Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Year', 'Total Shares', 'Year-End Value (VND)', 'Year-End Total Investment (VND)', 'Annual Investment (VND)', 'Annual Shares Held', 'Performance Percentage (%)'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[years, 
                           [f"{shares:.2f}" for shares in end_of_year_shares], 
                           [f"{value:,.2f}" for value in end_of_year_values], 
                           [f"{investment:,.0f}" for investment in end_of_year_investments],
                           [f"{annual_invest:,.0f}" for annual_invest in annual_investment],
                           [f"{annual_shares:.2f}" for annual_shares in annual_shares_held],
                           [f"{performance:.2f}" for performance in performance_percentage]],
                   fill_color='lavender',
                   align='left'))
    ])
    
    fig.update_layout(title='DCA Investment Performance Visualization')
    fig.show()

ticker = 'DCDS'
dca_final_performance_visualized(ticker, start_year=2010, end_year=2020)