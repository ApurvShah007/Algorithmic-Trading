import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import talib
import statsmodels.api as sm 
import time 
import yfinance as yf
import os

#I have imported and used functions from the previous files uploaded in this repository. Many functions are required 
#for many further implementations and further calculations. 
import rolling_stats as rs
import norm_dist as nd

def get_data_close(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="max")
    return pd.DataFrame(df['Close'])

def plot_hist_with_stats(stocks, dates, m = False, bins = 20):
    '''
    This function is useful for plotting histograms for one or more than one stock at a time. 
    This function takes in a list of stock symbols , the range of dates, whether to plot the mean of the stock or not. Default value is False.
    This function also takes in the number of bins required in the histogram, the default value is 20. 
    '''
    df_daily_all = pd.DataFrame(index = dates)
    alpha = 0.8
    for s in stocks:
        #Using the daily_return function from the rolling_stats.py file. 
        df_return = rs.daily_return(s, dates, False)
        df_return = df_return.rename(columns={'Daily Return' : s})
        df_daily_all = df_daily_all.join(df_return) 
        ax = df_daily_all[s].hist(bins=bins,  edgecolor='black', alpha = alpha, label=s)
        alpha-=0.3
        if m==False:
            continue
        else:
            mean = df_return[s].mean()
            plt.axvline(mean, color = 'black')
    plt.legend()
    plt.show()


def plot_scatter(stocks, dates):
    '''
    This function takes in a list of pair of stocks between which the alpha and beta is to be found and a line of best fit is to be plotted.
    The daily returns of both the stocks are calculated from the function from rolling_stats.py and then graphed against each other. This 
    function is mainly used to plot any stock against the S&P 500 or Dow Jones Index stocks to get a sens eof how well the stock is 
    doing with respect to the market and how reactive it is to the market movements. 
    This function accepts 2 para,eters : stocks - A list of lists of size 2, dates - The daterange for the scatter plot.
    '''
    for s in stocks:
        df_return1 = rs.daily_return(s[0], dates, False)
        df_return1 = df_return1.rename(columns= {"Daily Return": s[0]})
        df_return2 = rs.daily_return(s[1], dates, False)
        df_return2 = df_return2.rename(columns= {"Daily Return": s[1]})
        df_return = df_return1.join(df_return2)

        title = s[1] + ' vs ' + s[0]
        beta , alpha = np.polyfit(df_return[s[0]] , df_return[s[1]] , 1)
        df_return.plot(kind = 'scatter', x = s[0], y = s[1], edgecolor = 'black', title  = title)
        plt.plot(df_return[s[0]] , beta*df_return[s[0]] + alpha , color='red')
        print("Correlation of " , s[0], ' and ',  s[1], ' is: ')
        print(np.array(df_return.corr(method='pearson'))[0,1])
        plt.show()