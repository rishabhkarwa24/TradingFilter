import requests
from bs4 import BeautifulSoup
import pandas as pd

url1 = 'https://www.marketbeat.com/stocks/NASDAQ/'
url2 = '/institutional-ownership/'
url = ''
stockInfo = []


class Marketbeat:

    def readmarketdata(self, stock):
        """
        This method reads the marketbeat data for a stock
        :param stock: the name of the stock
        :return: NULL
        """
        global url
        # The URL that is created assuming stock belongs in NASDAQ
        # If failure occurs the stock is a part of NYSE, which a later part of the code handles
        url = url1 + stock + url2
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Getting the name of stock plus additional information
        results = soup.find('title').get_text()
        name = results.split()
        # Getting the ticker symobol (name[0]) and full name of the company(rest of code)
        name = name[0] + ' ' + results[results.find('('):results.find(')') + 1] + ': '

        # If answer4 does not exist, the stock html likely uses different formatting (both NYSE and NASDAQ)
        try:
            results = soup.find(id='answer4').get_text()
        except:
            return

        # Getting the two year share amount bought by institutions
        institutionalBuys2Year = results.split()
        institutionalBuys2Year = institutionalBuys2Year[7]

        # If answer6 does not exist, the stock html likely uses different formatting (both NYSE and NASDAQ)
        try:
            results = soup.find(id='answer6').get_text()
        except:
            return

        # Getting the two year share amount sold by institutions
        institutionalSells2Year = results.split()
        institutionalSells2Year = institutionalSells2Year[7]
        try:
            # If failure occurs here, the stock exists in the NYSE not NASDAQ (go to the except statement)
            twoYearRatio = int(institutionalBuys2Year.replace(',', '')) / int(institutionalSells2Year.replace(',', ''))

            institutionalBuys1Year = 0
            institutionalSells1Year = 0

            # Getting the one year buy and sell amount for the stock
            name_list = soup.find_all("div", class_='datapoint-heading mt-2 mb-1')
            for i in name_list:
                if i.get_text().find(" B") != -1:
                    if institutionalBuys1Year == 0:
                        institutionalBuys1Year = i.get_text()
                        institutionalBuys1Year = institutionalBuys1Year[1:-2]
                    if institutionalBuys1Year != 0:
                        institutionalSells1Year = i.get_text()
                        institutionalSells1Year = institutionalSells1Year[1:-2]
                        if (institutionalBuys1Year != institutionalSells1Year):
                             break

        # The stock exists in the NYSE, doing the same process for the stock
        except:
            # Changing url NASDAQ to NYSE
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

            institutionalBuys1Year = 0
            institutionalSells1Year = 0

            name_list = soup.find_all("div", class_='datapoint-heading mt-2 mb-1')
            for i in name_list:
                if i.get_text().find(" B") != -1:
                    if institutionalBuys1Year == 0:
                        institutionalBuys1Year = i.get_text()
                        institutionalBuys1Year = institutionalBuys1Year[1:-2]
                    if institutionalBuys1Year != 0:
                        institutionalSells1Year = i.get_text()
                        institutionalSells1Year = institutionalSells1Year[1:-2]
                        if (institutionalBuys1Year != institutionalSells1Year):
                            break

        # If the institutional sell amount could not be found, return from the function
        if (float(institutionalSells1Year) <= 0):
            return

        oneYearRatio = float(institutionalBuys1Year) / float(institutionalSells1Year)

        # If either condition is fulfilled, the stock has considerable institutional support
        if (twoYearRatio > 1 and oneYearRatio > 1.2) or oneYearRatio > 1.5:
            #print(name)
            twoYear = '2 Year Buy/Sell Ratio: ' + str(round(twoYearRatio, 2)) + ', '
            oneYear = '1 Year Buy/Sell Ratio: ' + str(round(oneYearRatio, 2))
            # Adding the stock info to the CSV file
            stockInfo.append((name + oneYear + twoYear))


    def institutionaldatatocsv(self):
        df = pd.DataFrame(stockInfo)
        # Moving all stock data to CSV
        df.to_csv('stock_info.csv', index=False, header=False, encoding='utf-8')
