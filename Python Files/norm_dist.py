import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import os
pd.options.display.float_format = '{:.5f}'.format

#Assumes that the csv file is in the same folder as the 
def symbol_to_path(symbol):
    return os.path.join("{}.csv".format(str(symbol)))

#This function treats the first ever recorded stock price to be the initial value and the rest of the ditribution is accordingly normalized. Then the selected date 
#range is sliced out and the plot is shown. 
#This function accepts the list of stocks and the date range of the required plot. 

def norm_dist(stocks, dates):
	df_exp = pd.DataFrame(index = dates)
	for s in stocks:
		path = symbol_to_path(s)
		df = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df = df.iloc[::-1]
		df = df.rename(columns = {"Adj Close" : s})
		#Normalizing the Ditribution
		df =(df)/df.iloc[-1]	
		print(df)
		df_exp = df_exp.join(df)
	df_exp.dropna(inplace = True)
	df_exp.plot()
	plt.show()
#This function first slices out the daterange provided and then uses the first value at the 0th row of the new sliced dataframe as the normalizing value and then 
#normalizes the entire ditribution based on that and then plots it. 
#This function accepts the list of stocks and the date range of the required plot. 
def norm_dist_yearwise(stocks, dates):
	df_exp = pd.DataFrame(index = dates)
	for s in stocks:
		path = symbol_to_path(s)
		df = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df = df.iloc[::-1]
		df = df.rename(columns = {"Adj Close" : s})
		df_exp = df_exp.join(df)
		df_exp = df_exp.dropna()
		#Normalizing the Ditribution
		df_exp= (df_exp)/df_exp.iloc[0]	
	df_exp.plot()
	plt.show()

#Smaple Run with n number of random stocks. Uncomment the following lines to see a sample run of the given functions. 
# dates = pd.date_range('2017-01-01','2017-12-31')
# stocks = ['AZPN', 'GOOGL']
# norm_dist_yearwise(stocks, dates)