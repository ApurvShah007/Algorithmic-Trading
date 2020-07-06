import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import os

#I have imported and used functions from the previous files uploaded in this repository. Many functions are required 
#for many further implementations and further calculations. 
import rolling_stats as rs
import norm_dist as nd

pd.options.display.float_format = '{:.3f}'.format

def symbol_to_path(symbol):
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))

def portfolio_val(portfolio , comp, dates , val, plot=False):
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

	stats_dic = {'mean': 0,"std":0}
	stats_dic['mean'] = df_daily['Daily Return'].values.mean()
	stats_dic['std'] = df_daily['Daily Return'].values.std()
	if (plot == True):
		f1 = plt.figure(1)
		df_port['Daily Return'].plot(title = "Daily Return of the Portfolio")
		f2 = plt.figure(2)
		df_port['Value'].plot(title = "Value of the Portfolio")
		plt.show()
	return df_port, stats_dic

#def sharpe_ratio(portfolio, comp , dates,val, rfi=0):




#sample run with a random portfolio
 
portfolio = ['MSFT', 'AZPN', 'NFLX', 'GOOGL']
composition = [0.4 , 0.4, 0.1, 0.1]
dates =pd.date_range('2017-01-01','2017-12-31')
start_val = 1000000
portfolio_val(portfolio, composition , dates, start_val, True)


