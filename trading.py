import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import json
from datetime import datetime

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

valid_data = [entry for entry in data['DCDS'] if entry[0] > 0]  # Timestamp for 1 AD
timestamps, prices = zip(*valid_data)
# timestamps, prices = zip(*data['DCDS'])
dates = [datetime.fromtimestamp(ts / 1000.0) for ts in timestamps]

df = pd.DataFrame({
    'Date': dates,
    'Price': prices
})

df.set_index('Date', inplace=True)

# Plot the stock price data
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Price'], label='DCDS Stock Price')
plt.title('DCDS Stock Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# fig = go.Figure()

# fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], mode='lines+markers', name='DCDS Stock Price'))

# # Enhancing the layout
# fig.update_layout(
#     title='DCDS Stock Price Over Time',
#     xaxis_title='Date',
#     yaxis_title='Price',
#     hovermode='closest'  # Enable hover in the closest point
# )

# fig.show()