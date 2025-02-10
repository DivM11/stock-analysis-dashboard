"""
Main Application file for Finance Dashboard App
"""
import yfinance as yf
import streamlit as st

def get_initial_tickr_list(tickr_type):
    """
    Get initial list of tickers
    """
    if tickr_type == "fund":
        return ["SPY", "VOO", "QQQ", "DIA", "ARKK"]  # Expanded ETF list
    elif tickr_type == "stock":
        return ["MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]
    return []

def get_frequency_list():
    """Get list of frequency choices."""
    return ["yearly", "quarterly"]

@st.cache_data
def fetch_financial_data(ticker, frequency):
    """Fetch financial data using yfinance."""
    stock = yf.Ticker(ticker)
    return {
        "earnings_history": stock.get_earnings_history().T,
        "income_stmt": stock.get_income_stmt(freq=frequency),
        "balance_sheet": stock.get_balance_sheet(freq=frequency),
        "analyst_price_targets": stock.get_recommendations()
    }

def plot_data(df, columns, title):
    """Plot selected columns from a dataframe using st.line_chart."""
    if df is not None and not df.empty and columns:
        st.subheader(title)
        st.line_chart(df.loc[columns].T)

def main():
    st.set_page_config(layout="wide")
    st.title("Finance Dashboard App")
    
    with st.sidebar:
        tickr_type = st.selectbox("Select ticker type", ["stock"])
        available_tickers = get_initial_tickr_list(tickr_type)
        selected_tickers = st.multiselect("Select tickers", options=available_tickers, default=available_tickers[:2])
        # Allow user to enter a custom ticker
        custom_tickers = st.text_input("Enter additional tickers as CSV:", "")
        custom_tickers = custom_tickers.split(",")
        selected_tickers = list(set(selected_tickers+custom_tickers))
        available_frequencies = get_frequency_list()
        frequency = st.selectbox("Select period", options=available_frequencies,index=0)
    
    fetch_data = st.button("Fetch Data")
    
    if "all_data" not in st.session_state:
        st.session_state.all_data = {}
    
    if fetch_data:
        st.session_state.all_data = {ticker: fetch_financial_data(ticker, frequency) for ticker in selected_tickers}
    
    selected_ticker = st.selectbox("Select a ticker to view data", selected_tickers if selected_tickers else ["None"])
    
    tabs = st.tabs(["Data", "Visualizations"])
    
    with tabs[0]:
        if selected_ticker in st.session_state.all_data:
            data = st.session_state.all_data[selected_ticker]
            
            with st.expander("Earnings History", expanded=False):
                st.dataframe(data["earnings_history"], use_container_width=True)
            
            with st.expander("Income Statement", expanded=False):
                st.dataframe(data["income_stmt"], use_container_width=True)
            
            with st.expander("Balance Sheet", expanded=False):
                st.dataframe(data["balance_sheet"], use_container_width=True)
            
            with st.expander("Analyst Price Targets", expanded=False):
                st.dataframe(data["analyst_price_targets"], use_container_width=True)
    
    with tabs[1]:
        if selected_ticker in st.session_state.all_data:
            data = st.session_state.all_data[selected_ticker]
            
            with st.expander("Earnings History Over Time", expanded=False):
                earnings_columns = st.multiselect("Select earnings columns", data["earnings_history"].index if data["earnings_history"] is not None else [])
                plot_data(data["earnings_history"], earnings_columns, "Earnings History Over Time")
            
            with st.expander("Balance Sheet Over Time", expanded=False):
                balance_columns = st.multiselect("Select balance sheet columns", data["balance_sheet"].index if data["balance_sheet"] is not None else [])
                plot_data(data["balance_sheet"], balance_columns, "Balance Sheet Over Time")
            
            with st.expander("Income Statement Over Time", expanded=False):
                income_columns = st.multiselect("Select income statement columns", data["income_stmt"].index if data["income_stmt"] is not None else [])
                plot_data(data["income_stmt"], income_columns, "Income Statement Over Time")
    
if __name__ == "__main__":
    main()