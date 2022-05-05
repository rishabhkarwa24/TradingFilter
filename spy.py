import requests
from bs4 import BeautifulSoup
import Marketbeat

# Pulling all S&P 500 stocks from wikipedia
stockList = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = BeautifulSoup(stockList.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker)
tickers = [s.replace('\n', '') for s in tickers]

marketbeat = Marketbeat.Marketbeat()
for i in range(0, len(tickers) - 1, 1):
    # Instance of Marketbeat that reads the tickers
    marketbeat.readmarketdata(tickers[i])

# Pushing the stocks to CSV
marketbeat.institutionaldatatocsv()
