import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

st.title("Stock Price Predictor")

# About section
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, pandas, numpy, tensorflow, plotly, yfinance, sklearn
* **Data source:** [Yahoo Finance](https://finance.yahoo.com/) via yfinance
* This app predicts stock prices using historical data and a pre-trained neural network model.
* It allows users to:
    - Enter a stock symbol to analyze
    - View historical stock data
    - Visualize stock prices with various moving averages
    - Compare original close prices with predicted close prices
* The app uses a 20-year historical dataset and a 70-30 train-test split for predictions.
""")

stock = st.text_input("Enter the Stock ID", "GOOG")

end = datetime.now()
start = datetime(end.year-20, end.month, end.day)

google_data = yf.download(stock, start, end)

model = load_model("Latest_stock_price_model.keras")
st.subheader("Stock Data")
st.dataframe(google_data, use_container_width=True)

splitting_len = int(len(google_data)*0.7)
x_test = pd.DataFrame(google_data.Close[splitting_len:])

# Calculate all MAs
google_data['MA_for_250_days'] = google_data.Close.rolling(250).mean()
google_data['MA_for_200_days'] = google_data.Close.rolling(200).mean()
google_data['MA_for_100_days'] = google_data.Close.rolling(100).mean()
google_data['MA_for_50_days'] = google_data.Close.rolling(50).mean()

# Create a multiselect for choosing MAs
st.subheader('Select Moving Averages to Display')
selected_mas = st.multiselect(
    'Choose Moving Averages',
    ['MA_for_250_days', 'MA_for_200_days', 'MA_for_100_days', 'MA_for_50_days'],
    default=['MA_for_100_days']
)

# Function to plot the graph
def plot_graph(full_data, selected_mas):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=full_data.index, y=full_data.Close, name='Close Price', line=dict(color='blue')))
    
    colors = ['orange', 'green', 'red', 'purple']
    for i, ma in enumerate(selected_mas):
        fig.add_trace(go.Scatter(x=full_data.index, y=full_data[ma], name=ma, line=dict(color=colors[i % len(colors)])))
    
    fig.update_layout(height=600, width=1000, title_text="Stock Price Analysis with Moving Averages")
    return fig

# Plot the graph with selected MAs
st.plotly_chart(plot_graph(google_data, selected_mas))

# Rest of your code remains the same
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(x_test[['Close']])

x_data = []
y_data = []

for i in range(100, len(scaled_data)):
    x_data.append(scaled_data[i-100:i])
    y_data.append(scaled_data[i])

x_data, y_data = np.array(x_data), np.array(y_data)

predictions = model.predict(x_data)

inv_pre = scaler.inverse_transform(predictions)
inv_y_test = scaler.inverse_transform(y_data)

ploting_data = pd.DataFrame(
    {
        'original_test_data': inv_y_test.reshape(-1),
        'predictions': inv_pre.reshape(-1)
    },
    index = google_data.index[splitting_len+100:]
)
st.subheader("Original values vs Predicted values")
st.dataframe(ploting_data, use_container_width=True)

st.subheader('Original Close Price vs Predicted Close price')
fig = go.Figure()
fig.add_trace(go.Scatter(x=google_data.index[:splitting_len+100], y=google_data.Close[:splitting_len+100], name='Data- not used', line=dict(color='gray')))
fig.add_trace(go.Scatter(x=ploting_data.index, y=ploting_data['original_test_data'], name='Original Test data', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=ploting_data.index, y=ploting_data['predictions'], name='Predicted Test data', line=dict(color='red')))
fig.update_layout(height=600, width=1000, title_text="Original vs Predicted Close Price")
st.plotly_chart(fig)