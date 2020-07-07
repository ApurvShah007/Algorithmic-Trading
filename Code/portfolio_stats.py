import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import math
import os

#I have imported and used functions from the previous files uploaded in this repository. Many functions are required 
#for many further implementations and further calculations. 
import rolling_stats as rs
import norm_dist as nd

pd.options.display.float_format = '{:.3f}'.format

def symbol_to_path(symbol):
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))



def portfolio_val(portfolio , comp, dates , val, plot=False):
	'''
	This function takes in 
	portfolio : a list of stocks in the portfolio
	comp : a list of composition of the portfolio
	dates : The range of date for which the request is to be observed
	val : The starting value of the portfolio at the start date in the date range
	plot : Whether you want to see the plot of daily returns and price

	This function returns a dataframe that has the value of each stock adjusted ny composition over the daterange, daily returns and 
	value of the portfolio, and a stats_dic which has the mean and std of the daily returns and the cumilative return over the 
	given date range. 
	'''
	df_norm  = pd.DataFrame(index = dates)

	for s in portfolio:
		df = pd.read_csv(symbol_to_path(s), index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df_temp = nd.norm_dist_yearwise(df , s, dates)
		df_norm = df_norm.join(df_temp)
		df_norm.dropna(inplace= True)

	df_norm = df_norm*comp*val
	df_norm['Value'] = df_norm.sum(axis=1)

	df_daily = rs.daily_return(df_norm, "Value", dates)
	df_daily= pd.DataFrame(df_daily['Daily Return'])
	df_port = df_norm.join(df_daily)
	df_daily = df_daily[1:]

	stats_dic = {'mean': 0,"std":0, 'cr':0}
	stats_dic['mean'] = df_daily['Daily Return'].values.mean()
	stats_dic['std'] = df_daily['Daily Return'].values.std()
	stats_dic['cr'] = ((df_port['Value'].iloc[-1]/df_port['Value'].iloc[0])-1)*100
	if (plot == True):
		f1 = plt.figure(1)
		df_port['Daily Return'].plot(title = "Daily Return of the Portfolio")
		f2 = plt.figure(2)
		df_port['Value'].plot(title = "Value of the Portfolio")
		plt.show()
	return df_port, stats_dic


def sharpe_ratio(portfolio, comp , dates,val, roi=0, recordings = 'Daily'):
	'''
	Sharpe Ratio = k*(mean(daily returns-roi)/ std(daily returns))
	k = sqrt(252)(Daily)
	k = sqrt(52)(Weekly)
	k = sqrt(12)(Monthly)
	k = 1 (Yearly)
	'''
	k = {'Daily': math.sqrt(252),'Weekly': math.sqrt(52), 'Monthly': math.sqrt(12)}
	delta = dates[-1]-dates[0]
	df_port , stats_dic = portfolio_val(portfolio, comp , dates, val)

	#Daily Recordings sharpe ratio
	df_daily = pd.DataFrame(df_port['Daily Return'])
	df_daily = df_daily[1:]
	df_daily = df_daily-roi
	sharpe_ratio = (df_daily["Daily Return"].values.mean()/stats_dic['std'])*k["Daily"]
	print(sharpe_ratio)






#sample run with a random portfolio


portfolio = ['MSFT', 'AZPN', 'NFLX', 'GOOGL']
composition = [0.4 , 0.4, 0.1, 0.1]
dates =pd.date_range('2017-01-01','2018-01-01')
start_val = 1000000
sharpe_ratio(portfolio, composition , dates, start_val)


