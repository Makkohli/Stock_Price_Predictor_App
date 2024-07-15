import streamlit as st
import pandas as pd
import base64
import plotly.graph_objects as go
import requests
import json

st.set_page_config(layout="wide")

st.title('Crypto Price')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrencies from CoinGecko!
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, plotly, requests, json
* **Data source:** [CoinGecko](https://www.coingecko.com/).
""")

col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header('Input Options')

# Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ['usd', 'btc', 'eth'])

@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency_price_unit,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame(data)
    df = df.rename(columns={
        "id": "coin_name",
        "symbol": "coin_symbol",
        "current_price": "price",
        "price_change_percentage_1h_in_currency": "percent_change_1h",
        "price_change_percentage_24h_in_currency": "percent_change_24h",
        "price_change_percentage_7d_in_currency": "percent_change_7d",
        "market_cap": "market_cap",
        "total_volume": "volume_24h"
    })
    
    return df[["coin_name", "coin_symbol", "market_cap", "percent_change_1h", "percent_change_24h", "percent_change_7d", "price", "volume_24h"]]

df = load_data()

## Sidebar - Cryptocurrency selections
sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin.head(num_coin)

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame', ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
# col2.write(f'Data Dimension: {df_selected_coin.shape[0]} rows and {df_selected_coin.shape[1]} columns.')

col2.dataframe(df_coins)

# Download CSV data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins['coin_symbol'], 
                       df_coins['percent_change_1h'], 
                       df_coins['percent_change_24h'], 
                       df_coins['percent_change_7d']], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

def create_plotly_bar(df, column, title):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=df.index,
            x=df[column],
            orientation='h',
            marker_color=['green' if x else 'red' for x in df[f'positive_{column}']],
        )
    )
    fig.update_layout(
        title=title,
        yaxis_title='Coin Symbol',
        xaxis_title='Percent Change',
        height=800,
    )
    return fig

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period*')
    fig = create_plotly_bar(df_change, 'percent_change_7d', '7 Days Percent Change')
    col3.plotly_chart(fig, use_container_width=True)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period*')
    fig = create_plotly_bar(df_change, 'percent_change_24h', '24 Hours Percent Change')
    col3.plotly_chart(fig, use_container_width=True)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period*')
    fig = create_plotly_bar(df_change, 'percent_change_1h', '1 Hour Percent Change')
    col3.plotly_chart(fig, use_container_width=True)