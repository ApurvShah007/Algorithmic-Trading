import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import os
pd.options.display.float_format = '{:.5f}'.format


def symbol_to_path(symbol):
    return os.path.join("{}.csv".format(str(symbol)))
def normalize (df):
	
	return df

def norm_dist(stocks, dates):
	df_exp = pd.DataFrame(index = dates)
	for s in stocks:
		path = symbol_to_path(s)
		df = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df = df.iloc[::-1]
		df = df.rename(columns = {"Adj Close" : s})
		#df = df['2020-04-01':'2004-08-19']
		print(df)
		print(df['2017-01-03'])
		df =(df)/df.iloc[-1]	
		print(df)
		df_exp = df_exp.join(df)

	df_exp = df_exp.dropna()
	df_exp.plot()
	plt.axhline(0, color='black')
	plt.show()

def norm_dist_yearwise(stocks, dates):
	df_exp = pd.DataFrame(index = dates)
	for s in stocks:
		path = symbol_to_path(s)
		df = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df = df.iloc[::-1]
		df = df.rename(columns = {"Adj Close" : s})
		df_exp = df_exp.join(df)
		df_exp = df_exp.dropna()
		df_exp= (df_exp)/df_exp.iloc[0]	

	df_exp.plot()
	plt.show()

#Smaple Run with n number of random stocks
dates = pd.date_range('2017-01-01','2017-12-31')
stocks = ['AZPN', 'GOOGL']
norm_dist_yearwise(stocks, dates)