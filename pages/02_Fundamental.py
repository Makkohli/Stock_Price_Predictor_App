import streamlit as st
import yfinance as yf
import plotly.express as px
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd



st.title('Stock Dashboard')

# About section
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, yfinance, plotly, numpy, pandas
* **Data source:** [Yahoo Finance](https://finance.yahoo.com/) via yfinance
* This app provides a comprehensive stock dashboard with the following features:
    - Historical stock price data visualization
    - Daily percentage change and volume graphs
    - Key statistics including annual return, standard deviation, and risk-adjusted return
    - Fundamental data including company overview, balance sheet, income statement, and cash flow
* Users can:
    - Input any stock ticker
    - Select custom date ranges for analysis
    - Toggle between pricing data and fundamental data views
* The dashboard offers interactive plots and styled statistics for enhanced user experience.
""")

# Sidebar inputs
ticker = st.sidebar.text_input('Ticker', 'GOOG')
start_date = st.sidebar.date_input('Start Date', datetime(2020, 1, 1))
end_date = st.sidebar.date_input('End Date', datetime.now())

# Download data
data = yf.download(ticker, start=start_date, end=end_date)

# Create tabs
pricing_data, fundamental_data = st.tabs(["Pricing Data", "Fundamental Data"])

with pricing_data:

    st.header('Price Movements')
    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.dataframe(data2, use_container_width=True)
    
    annual_return = data2['% Change'].mean() * 252 * 100
    stdev = np.std(data2['% Change']) * np.sqrt(252) * 100
    risk_adj_return = annual_return / stdev

    # Styling for the statistics
    st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        .stat-box {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .positive {
            background-color: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.2);
        }
        .negative {
            background-color: rgba(255, 0, 0, 0.1);
            border: 1px solid rgba(255, 0, 0, 0.2);
        }
        .neutral {
            background-color: rgba(0, 0, 255, 0.1);
            border: 1px solid rgba(0, 0, 255, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="stat-box {'positive' if annual_return > 0 else 'negative'}">
                <span class="big-font">Annual Return</span><br>
                {round(annual_return, 2)}%
            </div>
        """, unsafe_allow_html=True)

    with col2:
            st.markdown(f"""
            <div class="stat-box neutral">
                <span class="big-font">Standard Deviation</span><br>
                {round(stdev, 2)}%
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="stat-box {'positive' if risk_adj_return > 1 else 'negative'}">
                <span class="big-font">Risk Adj. Return</span><br>
                {round(risk_adj_return, 2)}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Create two columns for buttons
    col1, col2, col3, col4, col5 = st.columns(5)

     # Button to show the graph
    if col1.button('Show Daily % Change Graph'):
        # Create bar graph of % Change
        st.subheader('Daily Percentage Change')
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=data2.index,
            y=data2['% Change'] * 100,  # Convert to percentage
            name='Daily % Change'
            ))
        fig_bar.update_layout(
            title=f'{ticker} Daily Percentage Change',
            xaxis_title='Date',
            yaxis_title='Percentage Change (%)',
            barmode='relative'
            )
        st.plotly_chart(fig_bar)

        # Button to show the volume graph
    if col5.button('Show Volume Graph'):
        # Create bar graph of Volume
        st.subheader('Daily Trading Volume')
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume'
            ))
        fig_volume.update_layout(
                title=f'{ticker} Daily Trading Volume',
                xaxis_title='Date',
                yaxis_title='Volume',
                barmode='relative'
            )
        st.plotly_chart(fig_volume)


with fundamental_data:
    st.subheader(f'Overview of {ticker}')
    try:
        stock = yf.Ticker(ticker)
        overview_data = pd.DataFrame.from_dict(stock.info, orient='index', columns=[ticker])
        st.dataframe(overview_data, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching overview data: {e}")

    st.subheader('Balance Sheet')
    try:
        balance_sheet = stock.balance_sheet
        st.dataframe(balance_sheet, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching balance sheet data: {e}")

    st.subheader('Income Statement')
    try:
        income_statement = stock.financials
        st.dataframe(income_statement, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching income statement data: {e}")

    st.subheader('Cash Flow Statement')
    try:
        cash_flow = stock.cashflow
        st.dataframe(cash_flow, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching cash flow data: {e}")