# from contextlib import closing
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
import pandas_datareader.data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import math
import os

# from functions import recursive_prediction, select_model, create_model


def create_model(x_train):
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1)) # Prediction for the next day ( stock price )
    return model


def select_model(company_name, model):
    model.load_weights(f'machine_learning/taught_models/{company_name}/')


def recursive_prediction(predicted_prices, prediction_days, input_period, model):
    for i in range(input_period):
        next_day = [predicted_prices[predicted_prices.shape[0] - prediction_days:predicted_prices.shape[0] + 1, 0]]
        next_day = np.array(next_day)
        next_day = next_day.reshape(next_day.shape[0], next_day.shape[1], 1)

        prediction = model.predict(next_day)
        predicted_prices = np.append(predicted_prices, prediction)
        predicted_prices = predicted_prices.reshape(predicted_prices.shape[0], 1)
    return predicted_prices


def plot_data(actual_data, predicted_prices, company_name):
    dir = '../client/src/components/graph'
    plt.plot(actual_data, color='black', label=f'Actual Data')
    plt.plot(predicted_prices, color='red', label=f'Predicted Prices')
    plt.title(f'{company_name} shares')
    plt.xlabel('Time ( days )')
    plt.ylabel(f'{company_name} share price $')
    plt.legend()

    if os.path.isdir(dir) is False:
        os.mkdir(dir)

    plt.savefig(f'{dir}/plot.png')
    plt.close()


def activate_model(input_days, company):

    input_days = int(input_days)

    company = company.split(',')

    company_name = company[0]
    ticker_symbol = company[1]

    start = dt.datetime(1900, 1, 1)
    end = dt.datetime.now()

    data = web.DataReader(ticker_symbol, 'yahoo', start, end) # Ticker symbol !!!

    # Scaling data ( data / max_val )
    scale = max(data['Close'].values)
    closing_prices = data['Close'].values / scale
    closing_prices = closing_prices.reshape(len(closing_prices), 1)

    # How many days we want to take into account for prediction
    prediction_days = 30

    # 80 % of data goes for training, the rest for testing
    train_buffer = math.ceil(len(closing_prices) * 0.8)

    training_dataset = closing_prices[:train_buffer]
    test_dataset = closing_prices[train_buffer:]

    x_train = []
    x_labels = []

    # Assigning 30 previous days for every single unit
    for i in range(prediction_days, len(training_dataset)):
        x_train.append(training_dataset[i - prediction_days:i, 0])
        x_labels.append(training_dataset[i, 0])

    x_train, x_labels = np.array(x_train), np.array(x_labels)
    x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)

    model = create_model(x_train)

    model.load_weights(f'machine_learning/taught_models/{company_name}/')
    # select_model(company_name, model)

    ''' FOR TEACHING THE MODEL AND SAVING WEIGHTS '''
    # model.compile(optimizer='adam', loss='mean_squared_error')
    # model.fit(x_train, x_labels, epochs=30)

    # if os.path.isdir(f'machine_learning/taught_models/{company_name}') == False:
    #     os.mkdir(f'machine_learning/taught_models/{company_name}')

    # model.save_weights(f'machine_learning/taught_models/{company_name}/')

    actual_data = test_dataset * scale

    # Predicting already existing data and comparing both

    x_test = []

    for i in range(prediction_days, len(test_dataset)):
        x_test.append(test_dataset[i - prediction_days:i, 0])

    x_test = np.array(x_test)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)
    predicted_prices = model.predict(x_test)


    # Predicting the next x days and comparing them to actual share prices

    predicted_prices = recursive_prediction(predicted_prices, prediction_days, input_days, model)

    # Scaling back predicted prices for plotting
    predicted_prices *= scale

    plot_data(actual_data, predicted_prices, company_name)
