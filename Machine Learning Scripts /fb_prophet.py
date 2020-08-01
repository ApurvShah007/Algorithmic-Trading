import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
import yfinance as yf
import math

def fb_predict(symbol):
	stock = yf.Ticker(symbol)
	df = stock.history(period="max")
	df = df[['Open',  'High',  'Low',  'Close', 'Volume']]
	arr = [i for i in range(len(df))]
	ar = df.index
	df.index= arr
	df['ds'] = ar
	df = df[['ds', 'Close']]
	df.rename(columns = {"Close":'y'}, inplace = True)

	train_length = math.floor(0.1*len(df))
	train = df[:-train_length]
	test = df[-train_length:]
	m = Prophet(daily_seasonality = True) 
	m.fit(train) 
	future = m.make_future_dataframe(periods=train_length) #we need to specify the number of days in future
	prediction = m.predict(future)
	test_predict = prediction[-train_length:]
	test["predict"] = test_predict['trend']
	test["error"] =((test['y'] - test['predict'])/test['y'])*100
	mean_err = round(test['error'].mean(),3)
	

	mn = Prophet(daily_seasonality = True) 
	mn.fit(df) 
	future = mn.make_future_dataframe(periods=50) #we need to specify the number of days in future
	prediction = mn.predict(future)
	print(prediction)
	m.plot(prediction)
	plt.title("Prediction of the AZPN Stock Price using the Prophet")
	plt.xlabel("Date")
	plt.ylabel("Close Stock Price")
	plt.show()
	return mean_err



me = fb_predict("AZPN")
print("Mean Percentage Error : ", me)



