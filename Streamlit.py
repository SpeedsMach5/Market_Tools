import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objects as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

stocks = ("SPY")
selected_stocks = st.selectbox("Select dataset for prediction", stocks)

n_day = st.slider("Days of predicitons", 1,10)
period = n_day*10

@st.cache

def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace = True)
    return data

data_load_state = st.text("Raw Hunt Data")
data = load_data(selected_stocks)
data_load_state.text("Blood in the Water")

st.subheader("Raw Meat")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date":"ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader("Forecast")
st.write(forecast.tail())

st.write("Forecast Data")
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast Data")
fig2 = m.plot_components(forecast)
st.write(fig2)

