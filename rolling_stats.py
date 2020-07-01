import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import os

pd.options.display.float_format = '{:.3f}'.format


def symbol_to_path(symbol):
    return os.path.join("{}.csv".format(str(symbol)))

def daily_return(df):
 	df_return = df.copy()
 	df_return = df_return.rename(columns = {"Adj Close" : "Daily Return"})
 	df_return[1:] = (df[1:]/df[:-1].values)-1
 	df_return.iloc[0] = 0
 	df_return['Daily Return'] = df_return['Daily Return']*100
 	ax = df_return.plot(title = "Daily Returns Plot")
 	plt.show()


def cumulative_return(df):
 	df_cr = df.copy()
 	df_cr=df_cr.rename(columns = {"Adj Close" : "Cumilative Return"})
 	df_cr[1:] = (df[1:]/df.iloc[0])-1
 	df_cr.iloc[0] = 0
 	df_cr = df_cr['Cumilative Return']*100
 	ax = df_cr.plot(title = "Cumm Return")
 	plt.show()


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


#Sample Run
path = symbol_to_path('AZPN')
df_AZPN = pd.read_csv(path, index_col="Date",parse_dates=True, usecols=["Date", "Adj Close"])
df_AZPN = df_AZPN.iloc[::-1]

dates_2017 = pd.date_range('2017-01-01','2017-12-31')
df_2017 = pd.DataFrame(index = dates_2017)
df_2017 = df_2017.join(df_AZPN)
df_2017 = df_2017.dropna()
cumulative_return(df_2017)

