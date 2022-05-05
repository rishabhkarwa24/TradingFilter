# This class contains a Stock object which will be used in the future implementation as more fields may be needed.
import yfinance as yf
import datetime
from pandas.tseries.offsets import BDay


class Stock:

    def __init__(self, name, oneYearRatio, twoYearRatio, price, percentChange):
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
        self.price = price
        self.percentChange = percentChange


def getStockValue(name):
    """
        This method returns the current stock price and the change from close the last business day
        :param name: The name of the stock
        :return: the array holding the two values
        """
    # array that will hold current price as first element and percent change as second
    priceAndPercentChange = []
    stock = yf.Ticker(name)
    # The stock price currently
    price = stock.info['regularMarketPrice']
    priceAndPercentChange.append(price)
    yesterday = datetime.datetime.today() - BDay(1)
    # Get the two business day range of the stock
    stock_data = yf.download(name, start=yesterday, end=datetime.datetime.today(), progress=False)
    # percent change over the last two days
    percentChange = ((price - stock_data['Close'].values[0]) / stock_data['Close'].values[0]) * 100
    priceAndPercentChange.append(str(round(percentChange, 2)))
    return priceAndPercentChange
