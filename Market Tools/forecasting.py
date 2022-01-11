from fbprophet import Prophet
from fbprophet.plot import plot_plotly

def forecast(pricing_data, period):
    df_train = pricing_data[["Date", "Close"]]
    df_train = df_train.rename(columns={"Date":"ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period, freq='D')
    forecast = m.predict(future)

    #forecast.tail())

    fig1 = plot_plotly(m, forecast)

    fig2 = m.plot_components(forecast)
    return forecast, fig1, fig2