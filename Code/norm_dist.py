import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import yfinance as yf
import os

pd.options.display.float_format = '{:.5f}'.format

def get_data_close(symbol):
    '''
    This function uses the very convinient ticker object to get the latest data of the underlying stock passed in to this function
    '''
    stock = yf.Ticker(symbol)
    df = stock.history(period="max")
    return pd.DataFrame(df['Close'])


def norm_dist_yearwise(symbol, dates, plot=False):
    '''
    This function first slices out the daterange provided and then uses the first value at the 0th row of the new sliced dataframe as the normalizing value and then 
    normalizes the entire ditribution based on that and then plots it. 
    This function accepts the list of stocks and the date range of the required plot. 
    '''
    df = get_data_close(symbol)
    df_nor = pd.DataFrame(index = dates)
    df = df.rename(columns = {"Close" : symbol})
    df_nor = df_nor.join(df)
    df_nor = df_nor.dropna()
    #Normalizing the Ditribution
    df_nor= (df_nor)/df_nor.iloc[0]-1
    if (plot==True):
        df_nor.plot()
        plt.show()
    return df_nor



def norm_dist(symbol, dates, plot = False):
    '''    
    This function treats the first ever recorded stock price to be the initial value and the rest of the ditribution is accordingly normalized. Then the selected date 
    range is sliced out and the plot is shown. 
    This function accepts the list of stocks and the date range of the required plot. 
    '''
    df = get_data_close(symbol)
    df_nor = pd.DataFrame(index = dates)
    df = df.rename(columns = {"Close" : symbol})
    #Normalizing the Ditribution
    df =(df)/df.iloc[0]-1
    df_nor = df_nor.join(df)
    df_nor.dropna(inplace = True)
    if plot ==True:
        df_nor.plot()
        plt.show()
    return df_nor

