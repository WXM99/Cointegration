from cointegration import Cointegration as Coin

usa_stock = {"2020-1-1": 123, "2020-1-2": 124, "2020-1-3": 125, "2020-1-4": 126}
chn_stock = {"2020-1-1": 123, "2020-1-2": 122, "2020-1-3": 121, "2020-1-4": 120}

pair = Coin(chn_stock, usa_stock)
print(pair.coint())
print(pair.getSpreadPrice())
print(pair.getParas())