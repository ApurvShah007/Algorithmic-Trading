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
import norm_dist

pd.options.display.float_format = '{:.5f}'.format

def symbol_to_path(symbol):
    return os.path.join("/Users/apurvshah/Desktop/Algorithmic_trading/Data/{}.csv".format(str(symbol)))


#sample run with a random portfolio

portfolio = ['MSFT', 'AZPN', 'APPL', 'GOOGL']
composition = [0.4 , 0.3, 0.2, 0.1]