## 1 day 5% VaR for 1 put option with strike 300, 2 year on an MSFT stock

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import scipy.linalg as linalg
import pprint
from optionprice import Option

amazon = web.get_data_yahoo("MSFT",
                            start = "2020-04-20",
                            end = "2021-04-20")

amazon_returns = amazon['Adj Close'].pct_change()
amazon_values = amazon['Adj Close']
current_value = amazon_values.tail(1)[0]

returns_std = amazon_returns.std()

annualised_std = returns_std * np.sqrt(252)


option_now = Option(european=True,
                kind='put',
                s0=current_value,
                k=300,
                t=2,
                sigma=annualised_std,
                r=0.05,
                dv=0)

option_price = option_now.getPrice()

simulated_values = []
for i in range(1000):
    realized_return = np.random.normal(0, returns_std, 1)
    simulated_value = current_value *  (1 + realized_return)

    option_at_realization = Option(european=True,
                kind='put',
                s0=simulated_value[0],
                k=300,
                t=2,
                sigma=annualised_std,
                r=0.05,
                dv=0)

    simulated_price = option_at_realization.getPrice()
    simulated_values.append(simulated_price)

simulation = pd.DataFrame(simulated_values)
value_at_risk = option_price - simulation.quantile(0.05)

print(option_price)
print(value_at_risk)

