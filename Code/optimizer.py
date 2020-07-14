import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import time 
import yfinance as yf
import scipy.optimize as spo

pd.options.display.float_format = '{:.3f}'.format

def get_data_close(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="max")
    return pd.DataFrame(df['Close'])

'''Optimizers are algorithms that can:
1) Find the minimum values of functions
2) Build parameterized models for data
3) Refine the portfolio to maximise value
'''
def f(X):
	Y = (X-1.5)**2 + 0.5
	return Y

#Test Run 

Xguess = 2
min_res = spo.minimize(f, Xguess,method = 'SLSQP', options = {'disp':True})
print(min_res.x, min_res.fun)