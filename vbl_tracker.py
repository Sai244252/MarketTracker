import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="VBL SIP Tracker (Historical Monthly Close)", layout="wide")
st.title("Varun Beverages (VBL) SIP Tracker")
st.markdown("This tracker uses **historical month-end prices** to calculate SIP returns.")

# Constants
sip_amount = 5000
symbol = "VBL.NS"  # Yahoo Finance symbol for Varun Beverages
start_date = "2024-04-01"
months = pd.date_range(start=start_date, periods=12, freq='M')  # Month-end dates

# Fetch historical month-end prices
data = yf.download(symbol, start=start_date, end=months[-1].strftime('%Y-%m-%d'))
data = data.resample('M').last()  # Ensure month-end prices

# Generate SIP data
sip_data = []
total_units = 0

for i, month in enumerate(months):
    price_row = data.loc[data.index.month == month.month]
    if not price_row.empty:
        price = float(price_row['Close'].values[-1])
        units = sip_amount / price
        total_units += units
        invested = sip_amount * (i + 1)
        current_value = total_units * price
        gain_loss = current_value - invested
        sip_data.append([month.strftime('%b-%Y'), sip_amount, round(price, 2), round(units, 4), round(total_units, 4),
                         invested, round(current_value, 2), round(gain_loss, 2)])

# Display DataFrame
columns = ["Month", "Investment (₹)", "Price (₹)", "Units Bought", "Total Units",
           "Cumulative Investment (₹)", "Current Value (₹)", "Gain/Loss (₹)"]
df = pd.DataFrame(sip_data, columns=columns)
st.dataframe(df, use_container_width=True)

st.caption("Prices are pulled from Yahoo Finance using yfinance and represent the closing price at each month's end.")
