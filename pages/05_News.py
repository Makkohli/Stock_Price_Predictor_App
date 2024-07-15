from stocknews import StockNews
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Custom CSS for the card style
st.markdown("""
    <style>
    .news-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .news-title {
        font-size: 24px;
        font-weight: bold;
        color: black;
    }
    .news-date {
        font-size: 14px;
        color: gray;
        margin-bottom: 10px;
    }
    .news-summary {
        font-size: 18px;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# News section
st.title("News")

# About section
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, stocknews, pandas, numpy
* **Data source:** RSS feeds via StockNews library
* This app provides the latest news for a given stock ticker:
    - Users can input any stock ticker symbol
    - Displays up to 10 most recent news articles related to the stock
    - Each news item includes the title, publication date, and a summary
* The app aims to keep investors informed about the latest developments affecting their chosen stocks.
""")

ticker = st.text_input("Enter the Stock ID", "GOOG")

st.header(f'News of {ticker}')
sn = StockNews(ticker, save_news=False)
df_news = sn.read_rss()

def format_date(date_str):
    dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    return dt.strftime("%a, %d %b %Y %H:%M:%S")

for i in range(min(10, len(df_news))):
    with st.container():
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title">{df_news['title'][i]}</div>
                <div class="news-date">{format_date(df_news['published'][i])}</div>
                <div class="news-summary">{df_news['summary'][i]}</div>
            </div>
        """, unsafe_allow_html=True)
