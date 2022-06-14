from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import numpy as np


def create_model():
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
    model.load_weights(f'TaughtModels/{company_name}/')


def recursive_prediction(predicted_prices, prediction_days, input_period, model):
    for i in range(input_period):
        next_day = [predicted_prices[predicted_prices.shape[0] - prediction_days:predicted_prices.shape[0] + 1, 0]]
        next_day = np.array(next_day)
        next_day = next_day.reshape(next_day.shape[0], next_day.shape[1], 1)

        prediction = model.predict(next_day)
        predicted_prices = np.append(predicted_prices, prediction)
        predicted_prices = predicted_prices.reshape(predicted_prices.shape[0], 1)
    return predicted_prices