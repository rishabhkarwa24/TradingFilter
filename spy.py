import requests
from bs4 import BeautifulSoup
import Marketbeat
import yfinance as yf
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time

# Pulling all S&P 500 stocks from wikipedia
sp500 = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = BeautifulSoup(sp500.text, 'html.parser')
tableOfTickers = soup.find('tbody').get_text()

rawStockData = tableOfTickers.split()
tickers = []

# Words that get recognized as stocks, but are not stocks
# Working on a cleaner implementation of this process in order to avoid the extra runtime
garbageCollector = {'SEC', 'GICS', 'CIK', 'IT', 'UK', 'BNY', 'HP', 'IDEX', 'IHS', 'IPG', 'KLA', 'TE', 'SVB'}
for i in range(0, len(rawStockData) - 1, 1):
    if rawStockData[i].isupper() and len(rawStockData[i]) <= 4 and rawStockData[i].isalpha() and not rawStockData[i] in garbageCollector:
        if rawStockData[i - 1] != rawStockData[i]:
            tickers.append(rawStockData[i])
marketbeat = Marketbeat.Marketbeat()
for i in range(0, len(tickers) - 1, 1):
    # Instance of Marketbeat that reads the tickers
    marketbeat.readmarketdata(tickers[i])
# Pushing the stocks to CSV
marketbeat.institutionaldatatocsv()
