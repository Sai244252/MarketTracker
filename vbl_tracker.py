
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="VBL SIP Tracker", layout="wide")

st.title("Varun Beverages (VBL) SIP Tracker")
st.markdown("Track your monthly SIP investments with live stock prices fetched from Yahoo Finance.")

# Constants
sip_amount = 5000
stock_symbol = "VBL.NS"
start_date = "2024-04-01"
months = pd.date_range(start=start_date, periods=12, freq='MS').strftime('%b-%Y')

# Fetch live stock price
ticker = yf.Ticker(stock_symbol)
current_price = ticker.history(period="1d")['Close'].iloc[-1] if not ticker.history(period="1d").empty else 0
st.metric("Live VBL Price", f"₹{round(current_price, 2)}")

# SIP Tracker
sip_data = []
total_units = 0
for i, month in enumerate(months):
    price = current_price
    units = sip_amount / price if price else 0
    total_units += units
    invested = sip_amount * (i + 1)
    current_value = total_units * price
    gain_loss = current_value - invested
    sip_data.append([month, sip_amount, round(price, 2), round(units, 4), round(total_units, 4), invested, round(current_value, 2), round(gain_loss, 2)])

columns = ["Month", "Investment (₹)", "Stock Price (₹)", "Units Bought", "Total Units", "Cumulative Investment (₹)", "Current Value (₹)", "Gain/Loss (₹)"]
df = pd.DataFrame(sip_data, columns=columns)

st.dataframe(df, use_container_width=True)
