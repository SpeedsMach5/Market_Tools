from fbprophet import Prophet
from fbprophet.plot import plot_plotly, add_changepoints_to_plot
from matplotlib.pyplot import xlabel

def forecast(pricing_data, period):
    df_train = pricing_data[["Date", "Close"]]
    df_train = df_train.rename(columns={"Date":"ds", "Close": "y"})

    m = Prophet(changepoint_prior_scale=0.5, )
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period, freq='D')
    forecast = m.predict(future)

    #forecast.tail())

    fig1 = m.plot(forecast, xlabel="Date",ylabel="Price");add_changepoints_to_plot(fig1.gca(),  m, forecast)
    #a = add_changepoints_to_plot( m, forecast)

    fig2 = m.plot_components(forecast)
    return forecast, fig1, fig2