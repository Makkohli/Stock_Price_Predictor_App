# Stock Price Prediction Project

## Overview

This project is a comprehensive Streamlit application designed for stock price prediction and analysis. The main focus is on S&P 500 companies, but the app also includes features for cryptocurrency prices, news, and fundamental analysis to enhance the user experience.

## Project Structure

- **SP500.py**: The main file running on localhost, focused on S&P 500 stock data.
- **Stock Price Predictor.py**: Predicts stock prices using historical data and a pre-trained neural network model.
- **Fundamental.py**: Provides a comprehensive stock dashboard with historical price data visualization, daily percentage change, volume graphs, and key statistics.
- **CAPM.py**: Implements Capital Asset Pricing Model (CAPM) for calculating the expected return of selected stocks.
- **Crypto Price.py**: Retrieves cryptocurrency prices for the top 100 cryptocurrencies from CoinGecko.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Sources**: Wikipedia, Yahoo Finance (yfinance)
- **Libraries**: Pandas, NumPy, Matplotlib, Plotly, TensorFlow/Keras (for neural network model)
- **Visualization**: Matplotlib, Plotly
- **Deployment**: Streamlit Sharing


## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main Streamlit application:

    ```bash
    streamlit run SP500.py
    ```

## File Descriptions

### SP500.py

- **Libraries Used**: Streamlit, Pandas, Base64, Plotly, Seaborn, Numpy, Yfinance
- **Data Sources**: [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies), [Yahoo Finance](https://finance.yahoo.com/)
- **Features**:
  - Retrieves the list of S&P 500 companies and their stock closing prices (year-to-date).
  - Allows users to select sectors and companies to visualize stock price trends.

### Stock Price Predictor.py

- **Libraries Used**: Streamlit, Pandas, Numpy, TensorFlow, Plotly, Yfinance, Sklearn
- **Data Sources**: [Yahoo Finance](https://finance.yahoo.com/) via Yfinance
- **Features**:
  - Predicts stock prices using historical data and a pre-trained neural network model.
  - Users can enter a stock symbol to analyze, view historical stock data, visualize stock prices with various moving averages, and compare original close prices with predicted close prices.

### Fundamental.py

- **Libraries Used**: Streamlit, Yfinance, Plotly, Numpy, Pandas
- **Data Sources**: [Yahoo Finance](https://finance.yahoo.com/) via Yfinance
- **Features**:
  - Provides a comprehensive stock dashboard with historical stock price data visualization, daily percentage change and volume graphs, key statistics including annual return, standard deviation, and risk-adjusted return.
  - Fundamental data including company overview, balance sheet, income statement, and cash flow.

### CAPM.py

- **Libraries Used**: Streamlit, Pandas, Yfinance, Datetime, Pandas DataReader
- **Features**:
  - Implements Capital Asset Pricing Model (CAPM) for calculating the expected return of selected stocks.
  - Allows users to select up to 4 stocks and specify the number of years for historical data.

### Crypto Price.py

- **Libraries Used**: Streamlit, Pandas, Base64, Plotly, Requests, Json
- **Data Sources**: [CoinGecko](https://www.coingecko.com/)
- **Features**:
  - Retrieves cryptocurrency prices for the top 100 cryptocurrencies from CoinGecko.
  - Users can select the currency for price display, choose cryptocurrencies, and view price data, percentage changes, and download the data as a CSV file.

## Usage

1. **Run the Main App**:
    ```bash
    streamlit run SP500.py
    ```
2. **Navigate through the app** to explore different sections including stock price prediction, stock dashboard, CAPM, and cryptocurrency prices.
3. **Interact with the features** such as selecting sectors and companies, viewing historical stock data, predicting stock prices, and downloading data.

## Contributions

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

By integrating various financial analysis tools and data sources, this project aims to provide a comprehensive platform for stock price prediction and analysis, enriching the user experience with additional features like cryptocurrency tracking and fundamental analysis.
