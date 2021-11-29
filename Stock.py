# This class contains a Stock object which will be used in the future implementation
# as more fields may be needed. The tree implementation will also need a Stock object to find on search
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
        self.dailyChange = percentChange
