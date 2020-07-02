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

pd.options.display.float_format = '{:.5f}'.format

#Assumes that the csv file is in the same folder as the 
def symbol_to_path(symbol):
    return os.path.join("{}.csv".format(str(symbol)))


# This function is useful for plotting histograms for one or more than one stock at a time. 
# This function takes in a list of stock symbols , the range of dates, whether to plot the mean of the stock or not. Default value is False.
# This function also takes in the number of bins required in the histogram, the default value is 20. 
def plot_hist_with_stats(stocks, dates, m = False, bins = 20):
	df_daily_all = pd.DataFrame(index = dates)
	for s in stocks:
		path = symbol_to_path(s)
		df = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df = df.iloc[::-1]
		df = df.rename(columns = {"Adj Close" : s})
		#Using the daily_return function from the rolling_stats.py file. 
		df_return = rs.daily_return(df, dates, False)
		df_return.rename(columns={'Daily Return' : s})
		df_daily_all = df_daily_all.join(df_return) 
		ax = df_daily_all[s].hist(bins=bins,  edgecolor='black', alpha = 0.5, label=s)
		if m==False:
			continue
		else:
			mean = df_return[s].mean()
			plt.axvline(mean, color = 'black')
	plt.legend()
	plt.show()

#This function takes in a list of pair of stocks between which the alpha and beta is to be found and a line of best fit is to be plotted.
#The daily returns of both the stocks are calculated from the function from rolling_stats.py and then graphed against each other. This 
#function is mainly used to plot any stock against the S&P 500 or Dow Jones Index stocks to get a sens eof how well the stock is 
#doing with respect to the market and how reactive it is to the market movements. 

#This function accepts 2 para,eters : stocks - A list of lists of size 2, dates - The daterange for the scatter plot.
def plot_scatter(stocks, dates):
	for s in stocks:
		path = symbol_to_path(s[0])
		df1 = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df1=df1.iloc[::-1]
		path = symbol_to_path(s[1])
		df2 = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
		df2 = df2.iloc[::-1]

		df_return1 = rs.daily_return(df1, dates, False)
		df_return1 = df_return1.rename(columns= {"Daily Return": s[0]})
		df_return2 = rs.daily_return(df2, dates, False)
		df_return2 = df_return2.rename(columns= {"Daily Return": s[1]})
		df_return = df_return1.join(df_return2)

		title = s[1] + ' vs ' + s[0]
		beta , alpha = np.polyfit(df_return[s[0]] , df_return[s[1]] , 1)
		df_return.plot(kind = 'scatter', x = s[0], y = s[1], edgecolor = 'black', title  = title)
		plt.plot(df_return[s[0]] , beta*df_return[s[0]] + alpha , color='red')

		print(df_return.corr(method='pearson'))

	plt.show()



#Sample Run with a random stock. Uncomment the following lines to have a sample run for the above functions.
#dates = pd.date_range('2015-01-01','2017-12-31')
# plot_hist_with_stats(['MSFT', 'AZPN'], dates)
#plot_scatter([["MSFT", "AZPN"]], dates)
