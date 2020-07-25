import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as web
from datetime import datetime
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


#Taking an example portfolio of FAANG
portfolio = ['FB', "AAPL", "AMZN", 'NFLX', 'GOOG']
weights = np.array([0.2,0.2,0.2,0.2,0.2])
df = pd.DataFrame()
today = datetime.today().strftime('%Y-%m-%d')

#Getting the data
for stock in portfolio:
	df[stock] = web.DataReader(stock, data_source='yahoo', start = '2013-01-01', end = today)['Adj Close']
'''
#Plotting the portfolio
for stock in portfolio:
	plt.plot(df[stock], label=stock)
plt.title("Stocks ove given period")
plt.legend()
plt.show()
'''

#Calculating the essential Values for the portfolio

#Returns
returns = df.pct_change()
#Covariance
cov_matrix_annual = returns.cov() * 252
#Portfolio Varience
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
#Volatility
port_volatility = np.sqrt(port_variance)
#Annual Returns
portfolioSimpleAnnualReturn = np.sum(returns.mean()*weights) * 252
percent_var = str(round(port_variance, 2) * 100) + '%'
percent_vols = str(round(port_volatility, 2) * 100) + '%'
percent_ret = str(round(portfolioSimpleAnnualReturn, 2)*100)+'%'

print("Expected annual return : ", percent_ret)
print('Annual volatility/standard deviation/risk : ',percent_vols)
print('Annual variance : ',percent_var)
print("\n")

#Optimization 
mu = returns.mean() * 252
S = risk_models.sample_cov(df)
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = dict(ef.clean_weights())
print(cleaned_weights)
ef.portfolio_performance(verbose = True)
print("\n")

#Current best allocations
latest_prices = get_latest_prices(df)
#weights = cleaned_weights 
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=15000)
print(da)
allocation, leftover = da.lp_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))



