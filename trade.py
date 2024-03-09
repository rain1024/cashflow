import sqlite3
import pandas as pd
import plotly.graph_objects as go

def dca_annual_performance_visualized(ticker, start_year=2018, end_year=2023, monthly_investment=20000000):
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
    
    # Initialize dictionary to store annual results
    annual_performance = {}
    
    # Variables to accumulate totals for the final row
    total_investment_accum = 0
    total_shares_accum = 0
    final_value_accum = 0
    
    for year in range(start_year, end_year + 1):
        yearly_df = df[df.index.year == year]
        
        if not yearly_df.empty:
            yearly_df['shares_bought'] = monthly_investment / yearly_df['price']
            total_shares = yearly_df['shares_bought'].sum()
            total_investment = monthly_investment * len(yearly_df)
            final_price = yearly_df['price'].iloc[-1]
            final_value = total_shares * final_price
            investment_return = final_value - total_investment
            performance_percentage = (investment_return / total_investment) * 100
            
            # Accumulate totals
            total_investment_accum += total_investment
            total_shares_accum += total_shares
            final_value_accum += final_value
            
            annual_performance[year] = {
                'year': year,
                'total_investment': f"{total_investment:,.0f}",
                'total_shares': f"{total_shares:,.2f}",
                'final_value': f"{final_value:,.2f}",
                'investment_return': f"{investment_return:,.2f}",
                'performance_percentage': f"{performance_percentage:,.2f}"
            }
    
    # Calculate the accumulated row
    accumulated_performance = {
        'year': 'Total/Avg',
        'total_investment': f"{total_investment_accum:,.0f}",
        'total_shares': f"{total_shares_accum:,.2f}",
        'final_value': f"{final_value_accum:,.2f}",
        'investment_return': f"{final_value_accum - total_investment_accum:,.2f}",
        'performance_percentage': f"{((final_value_accum - total_investment_accum) / total_investment_accum) * 100:,.2f}"
    }
    
    # Add accumulated row to annual_performance
    annual_performance['Total/Avg'] = accumulated_performance
    
    # Convert the results dictionary to a DataFrame for visualization
    results_df = pd.DataFrame.from_dict(annual_performance, orient='index')
    
    # Use Plotly to create a table for visualization
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(results_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[results_df[k].tolist() for k in results_df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    fig.show()

# Example usage
ticker = 'DCDS'
dca_annual_performance_visualized(ticker, start_year=2010, end_year=2015)