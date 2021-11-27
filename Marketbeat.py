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
        name = name[0] + ' ' + results[results.find('('):results.find(')') + 1] + ': '

        try:
            results = soup.find(id='answer4').get_text()
        except:
            return

        institutionalBuys2Year = results.split()
        institutionalBuys2Year = institutionalBuys2Year[7]

        try:
            results = soup.find(id='answer6').get_text()
        except:
            return

        institutionalSells2Year = results.split()
        institutionalSells2Year = institutionalSells2Year[7]
        try:
            twoYearRatio = int(institutionalBuys2Year.replace(',', '')) / int(institutionalSells2Year.replace(',', ''))

            # Trying new marketbeat 1 year feature
            institutionalBuys1Year = 0
            institutionalSells1Year = 0

            name_list = soup.find_all("div", class_='datapoint-heading mt-2 mb-1')
            for i in name_list:
                if i.get_text().find(" B") != -1:
                    if institutionalBuys1Year == 0:
                        institutionalBuys1Year = i.get_text()
                        institutionalBuys1Year = institutionalBuys1Year[1:-2]
                        print('Institutional Buys: ' + institutionalBuys1Year)
                    if institutionalBuys1Year != 0:
                        institutionalSells1Year = i.get_text()
                        institutionalSells1Year = institutionalSells1Year[1:-2]
                        if (institutionalBuys1Year != institutionalSells1Year):
                             print('Institutional Sells: ' + institutionalSells1Year)
                             break

        except:
            print('NYSE')
            url = 'https://www.marketbeat.com/stocks/NYSE/' + stock + url2
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find('title').get_text()
            name = results.split()
            name = name[0] + ' ' + results[results.find('('):results.find(')') + 1] + ': '

            try:
                results = soup.find(id='answer4').get_text()
            except:
                return

            institutionalBuys2Year = results.split()
            institutionalBuys2Year = institutionalBuys2Year[7]

            try:
                results = soup.find(id='answer6').get_text()
            except:
                return

            institutionalSells2Year = results.split()
            institutionalSells2Year = institutionalSells2Year[7]


            try:
                twoYearRatio = int(institutionalBuys2Year.replace(',', '')) / int(institutionalSells2Year.replace(',', ''))
            except:
                return

            # Trying new marketbeat 1 year feature
            institutionalBuys1Year = 0
            institutionalSells1Year = 0

            name_list = soup.find_all("div", class_='datapoint-heading mt-2 mb-1')
            for i in name_list:
                if i.get_text().find(" B") != -1:
                    if institutionalBuys1Year == 0:
                        institutionalBuys1Year = i.get_text()
                        institutionalBuys1Year = institutionalBuys1Year[1:-2]
                        print('Institutional Buys: ' + institutionalBuys1Year)
                    if institutionalBuys1Year != 0:
                        institutionalSells1Year = i.get_text()
                        institutionalSells1Year = institutionalSells1Year[1:-2]
                        if (institutionalBuys1Year != institutionalSells1Year):
                            print('Institutional Sells: ' + institutionalSells1Year)
                            break

        if twoYearRatio > 1:
            print(name)
            buys = 'Shares Bought this Year: ' + institutionalBuys2Year + ', '
            sells = 'Shares Sold this Year: ' + institutionalSells2Year
            stockInfo.append((name + buys + sells))


    def institutionaldatatocsv(self):
        df = pd.DataFrame(stockInfo)
        df.to_csv('stock_info.csv', index=False, header=False, encoding='utf-8')
