import streamlit as st
from datetime import date
from fbprophet.plot import plot_plotly
from plotly import graph_objects as go
import pricing
import forecasting
import dmac_strategy
import ema_sma_crossover_strategy as ema_sma
import holoviews as hv
import macd_strategy
import matplotlib 
import buy_the_dip_function as bd

#CONFIGURATION
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
TICKER_LIST_PATH = 'data/constituents_symbols.txt'
STRATEGY_LIST_PATH = 'data/strategies.txt'
matplotlib.use('agg')

status = st.text("")

# UTILITY FUNCTIONS
def get_listbox_data(file_path):
    """Retrieves a list of data from a carriage return-delimited file

    Opens the file specified by the file path and returns a list of its contents.

    Parameters
    ----------
    file_path: str, required
        The path of the file containing the list of items
    
    """

    with open(file_path, "r") as file:
        content = file.read()
        content = content.split("\n")
        return content





# UI FLOW FUNCTIONS
def run_analysis(ticker, start_date, end_date, period, selected_strategies):
    """Runs and displays the different sections of the financial analysis

    Any code that needs to be run should have its own function and
    be called from here.  This is the main launch pad.  Order matters.

    Parameters
    ----------
    ticker: str, required
        A ticker symbol
    
    start_date: str, required
        Download start date string (YYYY-MM-DD) or _datetime
    
    end_date: str, required
        Download end date string (YYYY-MM-DD) or _datetime.
    
    period: int, required
        Number of periods to run the forecast

    selected_strategies: List, required
        List of strategies selected by the user. 
    """

    display_parameter_section()
    pricing_data = display_ticker_data_section(ticker, start_date, end_date)
    display_forecasting_section(pricing_data, period)
    # display_sentiment_indicators_section(pricing_data)
    # display_strategy_section(selected_strategies, pricing_data)





def display_parameter_section():
    """Displays a summary of the user-selected parameters
    
    """
    st.subheader("Parameters")
    st.write('Summary of parameter selections:')
    st.markdown('- Tickers: ' + ticker_selectbox)
    st.markdown('- Strategies: ' + str(strategy_listbox))
    st.markdown('- Prediction weeks: ' + str(n_day))
    st.warning("DISLCAIMER: This is for entertainment purposes only. This is NOT a solicitation to buy, sell or hold stocks, bonds or options. "\
        "By using this predictive tool you agree to hold harmless J2T (Just 2 Traders) and Fast Waters Trading for any financial losses incurred. "\
            "This tool uses the Prophet AI datasets that use 3 years of historic data for training and 1 year for predicitve modeling and PROSSIBLE future price realization. "\
                "This is a mean reverting model and does not account for event driven outcomes (news, sentiment, etc.) and DOES NOT model intraday movement. "\
                          
        )

    st.warning("README"\
        "The model outputs \
             1) Historic data (previous closes)= black dots \
                 2) Mean = blue line\
                     3) Trend changes = red line "\
                )

    st.warning("How to use"\
        "Select stock from drop down. There are currently 8,000 tradebale stocks listed. "\
            "Select number of weeks to model. You can model up to 4 weeks, but remember that the more time selected, the uncertainty is magnified."\
                "The predictive model graph is interactive zoom, pan, enlarge, etc. To reset graph select the 'home' icon (the house)"
    )  

    st.warning("Graph Interpretation"\
        "Closes that are away from the mean (blue line) are expected, but not garunteed, to revert to the mean at a point in the future. "\
            "The graph shows forward looking dates as possible time frames, not definitive time frames for price realization "\
            "Eaxmple: if a close is ABOVE the mean, the expected movement will be DOWN towards the mean at some point in the future."
                )

    st.warning("Expected Output"\
        "The last 5 days closing prices for the selected stock. "\
            "The predictive model price and the predicitve model graph. "\
                "Historic trend behavior for day of week, month of year and yearly trend." ) 

    st.warning("This tool is in beta and may be taken offline periodically for maintenance and or tuning without notice and for unknown lengths of time.")   
        
        





#@st.cache(suppress_st_warning=True)
def display_ticker_data_section(tickers, start_date, end_date, tail_records=5):
    """Retrieves and displays the Open, High, Low, Close prices 
    
    Retrieves and displays the Open, High, Low, and Close prices for the last
    X records in the DataFrame.

    Parameters
    ----------
    tickers: str, required
        A list of ticker symbols
    
    start_date: str, required
        Download start date string (YYYY-MM-DD) or _datetime
    
    end_date: str, required
        Download end date string (YYYY-MM-DD) or _datetime.
    
    tail_records: int, optional (Default = 5)
        Specifies the number of records to display

    """

    st.subheader(f"Ticker Data: Last {tail_records} Closes")
    status = st.info("Loading...")
    pricing_data = pricing.get_pricing_data(ticker_selectbox, start_date, end_date)
    status.empty()
    st.write(pricing_data.tail(tail_records))
    return pricing_data







#@st.cache(suppress_st_warning=True)
def display_forecasting_section(pricing_data, period):
    """Displays forecasting data

    Parameters
    ----------
    pricing_data: DataFrame, required
        Open, High, Low, Close data for a ticker
    
    """
    st.subheader("Forecasting")
    status = st.info("Loading...")

    forecast, fig1, fig2 = forecasting.forecast(pricing_data, period)

    st.warning("Note: These are probable outcomes, not an actual crystal ball")
    st.warning("Legend: Black dots = Close price, Blue line = Predicted price, Red line = Trend change")
    st.write(forecast.tail())

    st.plotly_chart(fig1)

    st.write(fig2)
    status.empty()





def display_sentiment_indicators_section(pricing_data):
    st.subheader("Sentiment Indicators")
    sentiment_status = st.info("Loading...")

    # SENTIMENT CODE HERE

    sentiment_status.empty()




def display_strategy_section(selected_strategies, pricing_data):
    """Displays the analysis of selected strategies

    The function loops through the strategies the user selected.  An 
    IF conditional structure has all of the possible supported strategies.
    

    Parameters
    ----------
    selected_strategies: List, required
        List of strategies the user selected
    
    """
    st.subheader("Analysis of Selected Strategies")
    strategy_status = st.info("Loading...")

    for strategy in selected_strategies:
        if strategy == 'Moving Averages Crossover':
            # call module and put presentation logic here 
            st.write("")
        elif strategy == 'Double Moving Average Crossover (DMAC)':
            st.write('__' + strategy + '__')
            
            # Creating the DMAC
            df, plot = dmac_strategy.analyze_dmac(pricing_data)
            st.write(df.tail())
            st.bokeh_chart(hv.render(plot, backend='bokeh'))

            #Backtesting the DMAC
            st.write("__ DMAC Backtest:__")
            df_backtest, plot = dmac_strategy.backtest_dmac(df)
            st.write(df_backtest.tail(1))
            st.bokeh_chart(hv.render(plot, backend='bokeh'))

        elif strategy == 'EMA SMA Crossover':
            st.write('__' + strategy + '__')
            
            # Backtesting the EMA SMA crossover
            df, results, plot = ema_sma.analyze_ema_sma_crossover(pricing_data)
            st.write(df.tail())

            st.write('Backtest:')
            st.write(f'Beginning balance: ${results[0]:,.2f}')
            st.write(f'Ending balance: ${results[1]:,.2f}')

            st.pyplot(plot)

        elif strategy == "Moving Average Convergence/Divergence (MACD)":
            st.write(strategy)

            # Creating the MACD
            df, plot = macd_strategy.analyze_macd(pricing_data)
            st.write(df.tail())
            st.bokeh_chart(hv.render(plot, backend='bokeh'))

            # Backtesting the MACD
            st.write("__MACD Backtest:__")
            df_backtest, plot = macd_strategy.backtest_macd(df)
            st.write(df_backtest.tail(1))
            st.bokeh_chart(hv.render(plot, backend="bokeh"))

        elif strategy == "Buy the Dip":

            # Creating Buy the Dip
            st.write('__' + strategy + '__')            
            df, results, plot = bd.buy_the_dip(pricing_data)
            st.write(df.tail())
            
            # Backtesting Buy the Dip
            st.write('Backtest:')
            st.write(f'Beginning balance: ${results[0]:,.2f}')
            st.write(f'Ending balance: ${results[1]:,.2f}')
            
            st.pyplot(plot)

    strategy_status.empty()





# LINEAR SIDEBAR UI
st.sidebar.subheader('Analysis Parameters')

status.text = "Loading ticker list"
ticker_list = get_listbox_data(TICKER_LIST_PATH)
ticker_selectbox = st.sidebar.selectbox("1. Choose a ticker", ticker_list)
st.sidebar.markdown('____')

strategy_list = get_listbox_data(STRATEGY_LIST_PATH)
strategy_listbox = st.sidebar.multiselect("2. Choose one or more trading strategies", strategy_list)
st.sidebar.markdown('____')

n_day = st.sidebar.slider("3. Choose number of weeks to forecast", 1,4)
period = n_day*10
st.sidebar.markdown('____')

st.sidebar.button('4. Run Analysis',
    key= 'button_run_analysis',
    help='Click to run analysis.', 
    on_click=run_analysis,
    args=(ticker_list, START, TODAY, period, strategy_listbox)
)
