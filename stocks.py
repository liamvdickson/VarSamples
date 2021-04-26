import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import scipy.linalg as linalg
import pprint

tickers = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]
weights = np.array([100, 50, 50, 200, 40])

stocks = web.get_data_yahoo(tickers,
                            start = "2020-03-01",
                            end = "2021-04-24")


multpl_stock_monthly_returns = stocks['Adj Close'].pct_change()
current = stocks['Adj Close'].tail(1)
current_portfolio_value = weights.dot(current.values[0])

cov = multpl_stock_monthly_returns.cov()
# cov= LU 
L = linalg.cholesky(cov, lower=True)
U = linalg.cholesky(cov, lower=False)

simulated_values = []
for i in range(10000):
    randomVector = np.random.normal(0, 1, 5)
    factors = np.matmul(L, randomVector) + np.array([1, 1, 1, 1, 1])
    simulated_value = np.multiply(current.values[0], factors)
    simulated_values.append(weights.dot(simulated_value))

simulation = pd.DataFrame(simulated_values)
value_at_risk = current_portfolio_value - simulation.quantile(0.05)
print(value_at_risk)

