import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Smart Portfolio Analyzer", layout="wide")

st.title("📊 Smart Portfolio Analyzer")
st.write("Analyze portfolio performance, risk, and return.")

# ---------- SESSION STATE ----------
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False


# ---------- USER INPUT ----------
tickers_input = st.text_input(
    "Enter Stock Tickers (comma separated)",
    "AAPL,MSFT,TSLA"
)

start_date = st.date_input(
    "Select Start Date",
    datetime(2022, 1, 1)
)

risk_free_rate = st.number_input(
    "Risk-Free Rate (%)",
    value=2.0
)

tickers = [t.strip().upper() for t in tickers_input.split(",")]

st.subheader("Investment Allocation")

investments = []
for ticker in tickers:
    amount = st.number_input(
        f"Investment in {ticker}",
        min_value=0.0,
        value=1000.0,
        key=f"inv_{ticker}"
    )
    investments.append(amount)


# ---------- ANALYZE BUTTON ----------
if st.button("Analyze Portfolio"):
    st.session_state.analyze_clicked = True


# ---------- MAIN PROGRAM ----------
if st.session_state.analyze_clicked:

    total_investment = sum(investments)

    if total_investment == 0:
        st.error("Total investment cannot be zero.")
        st.stop()

    weights = np.array(investments) / total_investment


    # ---------- VALIDATE TICKERS ----------
    valid_tickers = []
    invalid_tickers = []

    for ticker in tickers:
        test_data = yf.download(ticker, period="5d")

        if test_data.empty:
            invalid_tickers.append(ticker)
        else:
            valid_tickers.append(ticker)

    if invalid_tickers:
        st.error(f"Invalid ticker(s): {', '.join(invalid_tickers)}")
        st.stop()

    st.success(f"Valid tickers: {', '.join(valid_tickers)}")


    # ---------- FETCH STOCK DATA ----------
    data = yf.download(valid_tickers, start=start_date, auto_adjust=True)

    if data.empty:
        st.error("No data downloaded. Check tickers or internet connection.")
        st.stop()


    # ---------- HANDLE MULTI-INDEX ----------
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"]
    else:
        data = data[["Close"]]
        data.columns = valid_tickers


    # ---------- CALCULATE RETURNS ----------
    returns = data.pct_change().dropna(how="all")

    if returns.empty:
        st.error("Not enough data to calculate returns.")
        st.stop()

    portfolio_returns = returns.dot(weights)

    if portfolio_returns.empty:
        st.error("Portfolio return calculation failed.")
        st.stop()


    # ---------- PORTFOLIO METRICS ----------
    expected_return = portfolio_returns.mean() * 252
    volatility = portfolio_returns.std() * np.sqrt(252)

    sharpe_ratio = (expected_return - (risk_free_rate / 100)) / volatility

    var_95 = np.percentile(portfolio_returns, 5)

    cumulative_returns = (1 + portfolio_returns).cumprod()


    # ---------- DISPLAY METRICS ----------
    st.subheader("Portfolio Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Investment", f"${total_investment:,.2f}")
    col2.metric("Expected Annual Return", f"{expected_return*100:.2f}%")
    col3.metric("Annual Volatility", f"{volatility*100:.2f}%")
    col4.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

    st.metric("Value at Risk (95%) - Daily", f"{var_95*100:.2f}%")


    # ---------- CHARTS ----------
    st.subheader("Stock Price Trend")
    st.line_chart(data)

    st.subheader("Cumulative Portfolio Return")
    st.line_chart(cumulative_returns)


    # ---------- PORTFOLIO ALLOCATION PIE CHART ----------
    st.subheader("Portfolio Allocation")

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0E1117')   # dark outer bg
    ax.set_facecolor('white')  
    ax.pie(weights, labels=valid_tickers, autopct='%1.1f%%', textprops={'color': 'white'})
    ax.set_title("Investment Allocation", color='white')

    st.pyplot(fig)

