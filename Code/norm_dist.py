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
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))

#This function treats the first ever recorded stock price to be the initial value and the rest of the ditribution is accordingly normalized. Then the selected date 
#range is sliced out and the plot is shown. 
#This function accepts the list of stocks and the date range of the required plot. 

def norm_dist(stocks, symbol, dates, plot = False):
	df_nor = pd.DataFrame(index = dates)
	df = df.rename(columns = {"Adj Close" : s})
	#Normalizing the Ditribution
	df =(df)/df.iloc[0]	
	df_nor = df_nor.join(df)
	df_nor.dropna(inplace = True)
	if plot ==True:
		df_nor.plot()
		plt.show()
	else:
		return df_nor
	
#This function first slices out the daterange provided and then uses the first value at the 0th row of the new sliced dataframe as the normalizing value and then 
#normalizes the entire ditribution based on that and then plots it. 
#This function accepts the list of stocks and the date range of the required plot. 
def norm_dist_yearwise(df, symbol, dates, plot=False):
	df_nor = pd.DataFrame(index = dates)
	df = df.rename(columns = {"Adj Close" : symbol})
	df_nor = df_nor.join(df)
	df_nor = df_nor.dropna()
	#Normalizing the Ditribution
	df_nor= (df_nor)/df_nor.iloc[0]
	if (plot==True):
		df_nor.plot()
		plt.show()
	else:
		return df_nor

	

