import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import math
from keras import Sequential
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM, Dropout, Dense

def LSTM_model(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="max")
    df = df[['Open',  'High',  'Low',  'Close', 'Volume']]
    train_length = math.floor(0.1*len(df)) 
    train = df[:-train_length]
    test = df[-train_length:]
    training_set = train.iloc[:, 1: 2].values
    #print(training_set)
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    #print(training_set_scaled)
    X_train = []
    y_train = []
    for i in range(60, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-60: i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train) 
    X_train = np.reshape(X_train, newshape = (X_train.shape[0], X_train.shape[1], 1))
    regressor = Sequential()
    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    regressor.add(Dropout(rate = 0.2))
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(rate = 0.2))
    ##add 3rd lstm layer
    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(rate = 0.2))
    ##add 4th lstm layer
    regressor.add(LSTM(units = 50, return_sequences = False))
    regressor.add(Dropout(rate = 0.2))
    regressor.add(Dense(units = 1))
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
    regressor.fit(x = X_train, y = y_train, batch_size = 32, epochs = 10)
    real_stock_price = test.iloc[:, 1: 2].values
    dataset_total = pd.concat((train['Open'],test['Open']), axis = 0)
    inputs = dataset_total[len(dataset_total)-len(test)- 60: ].values
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, len(inputs)): 
        X_test.append(inputs[i-60: i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, newshape = (X_test.shape[0],X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    plt.plot(real_stock_price, color = 'red', label = 'Real price')
    plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted price')
    plt.title('{} price prediction'.format(symbol))
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

LSTM_model("AZPN")