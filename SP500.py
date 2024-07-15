import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('S&P 500')

# About section
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, plotly, seaborn, numpy, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies), [Yahoo Finance](https://finance.yahoo.com/)
* This app retrieves the list of S&P 500 companies and their stock closing prices (year-to-date).
* It allows users to select sectors and companies to visualize stock price trends.
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sector')

st.dataframe(df_selected_sector)

# Download S&P500 data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# Fetch stock data from yfinance
data = yf.download(
        tickers=list(df_selected_sector[:10].Symbol),
        period="ytd",
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )

# Plot Closing Price of Query Symbol using Plotly
def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.Date, y=df.Close, mode='lines', name=symbol))
    fig.update_layout(
        title=symbol,
        xaxis_title='Date',
        yaxis_title='Closing Price',
        template='plotly_white'
    )
    st.plotly_chart(fig)

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
