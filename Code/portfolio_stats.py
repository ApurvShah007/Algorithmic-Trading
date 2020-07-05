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

pd.options.display.float_format = '{:.5f}'.format

def symbol_to_path(symbol):
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))

def total_portfolio_val(portfolio , comp, dates ):
	df_norm  = pd.DataFrame(index = dates)

	for s in portfolio:
		df = pd.read_csv(symbol_to_path(s), index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df_temp = nd.norm_dist_yearwise(df , s, dates)
		df_norm = df_norm.join(df_temp)
		df_norm.dropna(inplace= True)
	print(df_norm.head())





#sample run with a random portfolio
 
portfolio = ['MSFT', 'AZPN', 'NFLX', 'GOOGL']
composition = [0.4 , 0.4, 0.1, 0.1]
dates =pd.date_range('2017-01-01','2017-12-31')
total_portfolio_val(portfolio, composition , dates)


# df1 = pd.read_csv(symbol_to_path(s[0]), index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
# df2 = pd.read_csv(symbol_to_path(s[1]), index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
# print(df1.head())
# print(df2.head())
# df_norm1 = nd.norm_dist_yearwise(df1 , s[0], dates)
# print(df_norm1.head())