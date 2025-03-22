
import streamlit as st
import pandas as pd

st.set_page_config(page_title="VBL SIP Tracker", layout="wide")

st.title("Varun Beverages (VBL) SIP Tracker - Based on Historical Order Prices")
st.markdown("This app uses real month-end prices (from order history) to track SIP investments.")

sip_amount = 5000
monthly_prices = {'Apr-2024': 15260.25, 'May-2024': 10944.0, 'Jun-2024': 4720.4, 'Jul-2024': 21467.55, 'Aug-2024': 6175.0, 'Sep-2024': 12414.0, 'Oct-2024': 3274.0, 'Nov-2024': 11527.92, 'Dec-2024': 17291.88, 'Jan-2025': 1672.5, 'Feb-2025': 1115.0, 'Mar-2025': 4391.87}

sip_data = []
total_units = 0

for i, (month, price) in enumerate(monthly_prices.items()):
    units = sip_amount / price if price else 0
    total_units += units
    invested = sip_amount * (i + 1)
    current_value = total_units * price
    gain_loss = current_value - invested
    sip_data.append([month, sip_amount, round(price, 2), round(units, 4), round(total_units, 4), invested, round(current_value, 2), round(gain_loss, 2)])

columns = ["Month", "Investment (₹)", "Stock Price (₹)", "Units Bought", "Total Units", "Cumulative Investment (₹)", "Current Value (₹)", "Gain/Loss (₹)"]
df = pd.DataFrame(sip_data, columns=columns)

st.dataframe(df, use_container_width=True)
