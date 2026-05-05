import matplotlib
matplotlib.use('Agg')  # Fix server issue

import matplotlib.pyplot as plt


def stock_price_chart(data):
    plt.figure()
    plt.plot(data['Close'])
    plt.title("Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.savefig("static/stock_chart.png")
    plt.close()
    return "stock_chart.png"  # return filename


def sentiment_chart(scores):
    plt.figure()

    if not isinstance(scores, dict) or sum(scores.values()) == 0:
        print("Using fallback sentiment data")
        scores = {"positive": 1, "negative": 1, "neutral": 1}

    labels = list(scores.keys())
    values = list(scores.values())

    plt.bar(labels, values, color=["green", "red", "gold"])
    plt.title("Sentiment Analysis")
    plt.savefig("static/sentiment_chart.png")
    plt.close()
    return "sentiment_chart.png"  # return filename
