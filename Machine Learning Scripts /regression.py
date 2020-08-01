import quandl, math
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime, timedelta
import yfinance as yf


style.use('ggplot')

def Regression(symbol):
	stock = yf.Ticker(symbol)
	df = stock.history(period="max")
	df = df[['Open',  'High',  'Low',  'Close', 'Volume']]
	df['HL_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
	df['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0
	arr = df['Close']
	df = df[['Close', 'HL_PCT', 'PCT_change', 'Volume']]
	forecast_col = 'Close'
	df.fillna(value=-99999, inplace=True)
	forecast_out = int(math.ceil(0.1 * len(df)))
	df['label'] = df[forecast_col].shift(-forecast_out)


	X = np.array(df.drop(['label','Close'], 1))
	X = preprocessing.scale(X)
	X_lately = X[-forecast_out:]
	X = X[:-forecast_out]

	df.dropna(inplace=True)
	y = np.array(df['label'])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	clf = LinearRegression(n_jobs=-1)
	clf.fit(X_train, y_train)

	confidence = clf.score(X_test, y_test)
	print(confidence)
	forecast_set = clf.predict(X_lately)
	df['Forecast'] = np.nan

	last_date = df.iloc[-1].name
	last_unix = last_date
	next_unix = last_unix + timedelta(days=1)

	for i in forecast_set:
	    next_date = next_unix
	    next_unix += timedelta(days=1)
	    j= [np.nan for _ in range(len(df.columns)-1)]+[i]
	    df.loc[next_date]=j
	#print(df.head())
	arr.plot()
	df['Forecast'].plot()
	plt.legend(loc=4)
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title("Forcast vs Actual price")
	plt.show()


Regression("FB")



