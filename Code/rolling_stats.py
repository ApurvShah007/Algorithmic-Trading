import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import os

pd.options.display.float_format = '{:.3f}'.format


#This file is to be used for further biuild upon the given functions. These functions are commonly used in many regular 
#computations. These are some of the common functions


#Assumes that the csv file is in the same folder as the 
def symbol_to_path(symbol):
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))


#This function returns or plots the daily returns of a given stock for a given time period. 
#This function accepts 3 parameters. df - the historic dataframe of the stock, date- the daterange for the plot, plot - a boolean for
#whether the user wnats to see the plot or just wants the resulting dataframe.  

def daily_return(df,dates, plot):
	df_return = df.copy()
	df_exp = pd.DataFrame(index = dates)
	df_exp = df_exp.join(df_return)
	df_exp.dropna(inplace = True)
	df_return = df_exp
	df_return = df_return.rename(columns = {"Adj Close" : "Daily Return"})
	df_return[1:] = (df_exp[1:]/df_exp[:-1].values)-1
	df_return.iloc[0] = 0
	if(plot==True):
 		df_return['Daily Return'] = df_return['Daily Return']*100
 		df_return['Daily Return'].plot(title = "Daily Returns")
 		plt.show()
	if (plot==False): 
 		return df_return

#This function returns or plots the cumilative returns of a given stock for a given time period. 
#This function accepts 3 parameters. df - the historic dataframe of the stock, date- the daterange for the plot, plot - a boolean for
#whether the user wnats to see the plot or just wants the resulting dataframe.  
#This function treats the first reading of the diven daterange as 0 and calculates the returns with respect to that date. 
def cumulative_return(df,date,plot):
 	df_cr = df.copy()
 	df_cr=df_cr.rename(columns = {"Adj Close" : "Cumilative Return"})
 	df_exp = pd.DataFrame(index = dates)
 	df_exp = df_exp.join(df_return)
 	df_cr[1:] = (df_exp[1:]/df_exp.iloc[0])-1
 	df_cr.iloc[0] = 0
 	if (plot==False):
 		return df_cr
 	else:
 	 	df_cr = df_cr['Cumilative Return']*100
 	 	ax = df_cr.plot(title = "Cumm Return")
 	 	plt.show()


#This function calculates the bollinger bands for the given stock in the given time period. These bands are powerful indicators for 
#making the decision for selling and buying. This should not be your only indicator but it certainly helps to visualize the data and trends.
#The upper bound is mean+2*std and the lower bound is mean-2*std. These lines are plotted on the graph along with the prices. 
#The rolling mean and rolling std is calculated for the past 20 days. 
def bollinger_bands(df):
	rm = df.rolling(20).mean()
	rstd =df.rolling(20).std()
	ub = rm+ 2*rstd
	lb = rm- 2*rstd
	ax = df.plot(title = "Bollinger Bounds")
	rm=rm.rename(columns = {"Adj Close" : "Rolling Mean "})
	rm.plot(label = "Rolling Mean", ax=ax)
	ub=ub.rename(columns = {"Adj Close" : "Upper Bound"})
	ub.plot(label = "Upper Bound", ax=ax)
	lb=lb.rename(columns = {"Adj Close" : "Lower Bound"})
	lb.plot(label = "Lower Bound", ax=ax)
	plt.show()


#Sample Run with a random stock

# path = symbol_to_path('AZPN')
# df_AZPN = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
# df_AZPN = df_AZPN.iloc[::-1]

# dates_2017 = pd.date_range('2017-01-01','2017-12-31')
# df_2017 = pd.DataFrame(index = dates_2017)
# df_2017 = df_2017.join(df_AZPN)
# df_2017 = df_2017.dropna()
# cumulative_return(df_2017)

