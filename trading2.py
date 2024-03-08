import pandas as pd
import plotly.graph_objs as go
import json
from datetime import datetime
import plotly.graph_objects as go

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

valid_data = [entry for entry in data['DCDS'] if entry[0] > 0]  # Timestamp for 1 AD
timestamps, prices = zip(*valid_data)
dates = [datetime.fromtimestamp(ts / 1000.0) for ts in timestamps]

df = pd.DataFrame({
    'Date': dates,
    'Price': prices
})

# df.set_index('Date', inplace=True)

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], mode='lines+markers', name='DCDS Stock Price'))

# Enhancing the layout
fig.update_layout(
    title='DCDS Stock Price Over Time',
    xaxis_title='Date',
    yaxis_title='Price',
    hovermode='closest',  # Enable hover in the closest point
    xaxis_tickformat='%d/%m/%Y'  # Setting the datetime format to yyyy/mm/dd
)

fig.show()