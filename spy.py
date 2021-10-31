import requests
from bs4 import BeautifulSoup
import Marketbeat
import yfinance as yf
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time

sp500 = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = BeautifulSoup(sp500.text, 'html.parser')
tableOfTickers = soup.find('tbody').get_text()
rawStockData = tableOfTickers.split()
tickers = []
garbageCollector = {'SEC', 'GICS', 'CIK', 'IT', 'UK', 'BNY', 'HP', 'IDEX', 'IHS', 'IPG', 'KLA', 'TE', 'SVB'}
for i in range(0, len(rawStockData) - 1, 1):
    if rawStockData[i].isupper() and len(rawStockData[i]) <= 4 and rawStockData[i].isalpha() and not rawStockData[i] in garbageCollector:
        if tickers[i - 1] == tickers[i]:
            i = i + 1
        tickers.append(rawStockData[i])
marketbeat = Marketbeat.Marketbeat()
#print(tickers)
for i in range(0, len(tickers) - 1, 1):
    marketbeat.readmarketdata(tickers[i])
marketbeat.institutionaldatatocsv()
