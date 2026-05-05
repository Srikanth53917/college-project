import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import time

STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)


def plot_stock_chart(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'])
    plt.title("Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")

    file_path = os.path.join(STATIC_FOLDER, f"stock_{int(time.time())}.png")
    plt.savefig(file_path)
    plt.close()

    return file_path


def plot_sentiment_chart(sentiment_counts):
    plt.figure(figsize=(6, 4))

    labels = ['Positive', 'Negative', 'Neutral']
    values = [
        sentiment_counts.get('positive', 0),
        sentiment_counts.get('negative', 0),
        sentiment_counts.get('neutral', 0)
    ]

    plt.bar(labels, values)

    file_path = os.path.join(STATIC_FOLDER, f"sentiment_{int(time.time())}.png")
    plt.savefig(file_path)
    plt.close()

    return file_path
