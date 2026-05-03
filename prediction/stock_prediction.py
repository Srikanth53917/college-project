import numpy as np
from sklearn.linear_model import LinearRegression

def train_stock_model(data):
    data = data.reset_index()

    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_next_day(model, data):
    next_day = len(data)
    prediction = model.predict([[next_day]])
    return float(prediction[0])
