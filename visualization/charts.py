import matplotlib.pyplot as plt
import os

def stock_price_chart(data, ticker):
    try:
        plt.figure(figsize=(8,4))
        plt.plot(data['Close'], label='Close Price')
        plt.title(f"{ticker} Stock Price")
        plt.legend()

        path = "static/stock_chart.png"
        plt.savefig(path)
        plt.close()

        return path
    except Exception as e:
        print("Chart error:", e)
        return None


def sentiment_chart(sentiment_score):
    try:
        labels = ['Negative', 'Neutral', 'Positive']
        values = [
            max(0, -sentiment_score),
            1 - abs(sentiment_score),
            max(0, sentiment_score)
        ]

        plt.figure(figsize=(5,5))
        plt.pie(values, labels=labels, autopct='%1.1f%%')

        path = "static/sentiment_chart.png"
        plt.savefig(path)
        plt.close()

        return path
    except Exception as e:
        print("Sentiment chart error:", e)
        return None
