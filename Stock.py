# This class contains a Stock object which will be used in the future implementation as more fields may be needed.
# The tree implementation will also need a Stock object to find on search
import dateutil.utils
import yfinance as yf
import datetime
from pandas.tseries.offsets import BDay
import time
import requests
import io
import seaborn as sns


class Stock:

    def __init__(self, name, oneYearRatio, twoYearRatio, percentChange):
        """
        The following parameters are needed to make a Stock object
        :param name: the name of the stock
        :param oneYearRatio: the one year buy to sell ratio of the stock
        :param twoYearRatio: the two year buy to sell ratio of the stock
        :param percentChange: the daily percent change of the stock
        """
        self.name = name
        self.oneYearRatio = oneYearRatio
        self.twoYearRatio = twoYearRatio
        self.percentChange = percentChange

    def getStockValue(self, name):
        """
        This method returns the current stock price and the change from close the last business day
        :param name: The name of the stock
        :return: the array holding the two values
        """
        #array that will hold current price as first element and percent change as second
        priceAndPercentChange = []
        stock = yf.Ticker(name)
        # The stock price currently
        price = stock.info['regularMarketPrice']
        priceAndPercentChange.append(price)
        yesterday = datetime.datetime.today() - BDay(1)
        stock_data = yf.download("ABBV", start=yesterday, end=datetime.datetime.today(), progress=False)
        val = stock_data['Open'].values[1]
        priceAndPercentChange.append(val)
        return priceAndPercentChange

s = Stock('ABBV', 1, 2, 4)
s.getStockValue('ABBV')
#tickers = ['ABBV']
#for ticker in tickers:
#    ticker_yahoo = yf.Ticker(ticker)
#    data = ticker_yahoo.history()
#    last_quote = (data.tail(1)['Close'].iloc[0])
#    print(ticker,last_quote)

#yesterday = datetime.datetime.today() - BDay(1)
#print(yesterday)
#stock = yf.download("ABBV", start=yesterday, end=datetime.datetime.today(), progress=False)
#print(stock)
#val = stock['Open'].values[1]
#print(val)