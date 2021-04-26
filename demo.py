# 1 MSFT stock 1-day 5% var

import pandas_datareader as web 
from statistics import NormalDist

stocks = web.get_data_yahoo('MSFT', "2020-04-22", "2021-04-22")

print(stocks.tail(1))

current = stocks['Adj Close'].tail(1)

print(current)

returns = stocks['Adj Close'].pct_change()

std = returns.std()

print(std)

dist = NormalDist(0, std)

var_return = dist.inv_cdf(0.95)

var_stock = (1 + var_return) * current

var_loss = current - var_stock

print(var_loss)