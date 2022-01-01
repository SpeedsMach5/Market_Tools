import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objects as go
import pandas as pd
from patterns import patterns
import os

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# ticker function
def read_tickers():
    with open("data/constituents_symbols.txt", "r") as file:
        content = file.read()
        content = content.split("\n")
        return content

# Number of days to calculate

stocks = (read_tickers())
selected_stocks = st.sidebar.selectbox("Hunting the Markets", stocks)

n_day = st.slider("Days of predicitons", 1,10)
period = n_day*10



@st.cache

def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace = True)
    return data

data_load_state = st.text("Raw Hunt Data")
data = load_data(selected_stocks)
data_load_state.text("This is for entertainment purposes only and not a solicitation to buy or sell stocks.")

st.subheader("Ticker Data for the past five closes")
st.write(data.tail())

#plot

def plot_raw_data():
    fig = go.Figure()
    #fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
    fig.layout.update(title_text="Closes", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig,use_container_width=True)

plot_raw_data()

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date":"ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader("Probable outcome, not an actual crystal ball")
st.write(forecast.tail())

st.write("Forecast Data")
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast Data")
fig2 = m.plot_components(forecast)
st.write(fig2)



