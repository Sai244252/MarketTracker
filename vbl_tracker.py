import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="VBL SIP Tracker (Excel Based)", layout="wide")
st.title("Varun Beverages (VBL) SIP Tracker")
st.markdown("Upload your order history Excel to track SIP performance based on actual transactions.")

# Upload Excel file
uploaded_file = st.file_uploader("Upload VBL Order History Excel", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_orders = pd.read_csv(uploaded_file)
        else:
            try:
                import openpyxl
                df_orders = pd.read_excel(uploaded_file, engine='openpyxl')
            except ImportError:
                st.error("The app requires the 'openpyxl' module to read Excel files. Please upload a CSV file or contact the developer.")
                st.stop()


        df_orders['Date'] = pd.to_datetime(df_orders['Date'])
        df_orders.sort_values(by='Date', inplace=True)

        # Calculate derived metrics
        df_orders['Units'] = df_orders['Invested'] / df_orders['Price']
        df_orders['Cumulative Units'] = df_orders['Units'].cumsum()
        df_orders['Cumulative Investment'] = df_orders['Invested'].cumsum()

        # Get latest price (assume from last row's price or future integration)
        latest_price = df_orders.iloc[-1]['Price']
        df_orders['Current Value'] = df_orders['Cumulative Units'] * latest_price
        df_orders['Gain/Loss'] = df_orders['Current Value'] - df_orders['Cumulative Investment']

        st.dataframe(df_orders, use_container_width=True)

        st.metric("Total Investment", f"₹{df_orders['Cumulative Investment'].iloc[-1]:,.2f}")
        st.metric("Total Units", f"{df_orders['Cumulative Units'].iloc[-1]:,.4f}")
        st.metric("Current Value", f"₹{df_orders['Current Value'].iloc[-1]:,.2f}")
        st.metric("Gain / Loss", f"₹{df_orders['Gain/Loss'].iloc[-1]:,.2f}")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload an Excel or CSV file containing your order history.")
