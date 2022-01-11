import yfinance as yf
import pandas as pd

def get_pricing_data(tickers, start_date, end_date):
    """Retrieves pricing historical pricing data for a list of tickers

    Utilizes yfinance to return pricing data between a start and end date.

    Parameters
    ----------
    tickers: str, required
        A list of ticker symbols
    
    start_date: str, required
        Download start date string (YYYY-MM-DD) or _datetime
    
    end_date: str, required
        Download end date string (YYYY-MM-DD) or _datetime.
    
    """
    data = yf.download(tickers, start_date, end_date)
    data.reset_index(inplace = True)
    return data