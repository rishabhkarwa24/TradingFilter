import requests
from bs4 import BeautifulSoup
import pandas as pd

url1 = 'https://www.marketbeat.com/stocks/NASDAQ/'
url2 = '/institutional-ownership/'
url = ''
stockInfo = []


class Marketbeat:

    def readmarketdata(self, stock):
        global url
        url = url1 + stock + url2
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find('title').get_text()
        name = results.split()
        name = name[0] + ' ' + name[6] + ': '

        try:
            results = soup.find(id='answer4').get_text()
        except:
            return
        institutionalBuys = results.split()
        institutionalBuys = institutionalBuys[7]

        try:
            results = soup.find(id='answer6').get_text()
        except:
            return
        institutionalSells = results.split()
        institutionalSells = institutionalSells[7]
        try:
            buySellRatio = int(institutionalBuys.replace(',', '')) / int(institutionalSells.replace(',', ''))
        except:
            url = 'https://www.marketbeat.com/stocks/NYSE/' + stock + url2
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find('title').get_text()
            name = results.split()
            name = name[0] + ' ' + name[6] + ': '

            try:
                results = soup.find(id='answer4').get_text()
            except:
                return
            institutionalBuys = results.split()
            institutionalBuys = institutionalBuys[7]

            try:
                results = soup.find(id='answer6').get_text()
            except:
                return
            institutionalSells = results.split()
            institutionalSells = institutionalSells[7]

            try:
                buySellRatio = int(institutionalBuys.replace(',', '')) / int(institutionalSells.replace(',', ''))
            except:
                return
        print(name)
        if buySellRatio > 1:
            buys = 'Shares Bought this Year: ' + institutionalBuys + ', '
            sells = 'Shares Sold this Year: ' + institutionalSells
            stockInfo.append((name + buys + sells))


    def institutionaldatatocsv(self):
        df = pd.DataFrame(stockInfo)
        df.to_csv('stock_info.csv', index=False, header=False, encoding='utf-8')
