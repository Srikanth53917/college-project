import matplotlib.pyplot as plt
import os

# Ensure static folder exists
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)


# 📈 STOCK PRICE CHART
def plot_stock_chart(data):
    try:
        plt.figure(figsize=(10, 5))

        # Plot closing price
        plt.plot(data['Close'], label='Close Price', color='blue')

        plt.title("Stock Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)

        # Save image
        file_path = os.path.join(STATIC_FOLDER, "stock_chart.png")
        plt.savefig(file_path)
        plt.close()

        return file_path

    except Exception as e:
        print("Error in plot_stock_chart:", e)
        return None


# 📊 SENTIMENT ANALYSIS CHART
def plot_sentiment_chart(sentiment_counts):
    try:
        plt.figure(figsize=(6, 4))

        labels = ['Positive', 'Negative', 'Neutral']
        values = [
            sentiment_counts.get('positive', 0),
            sentiment_counts.get('negative', 0),
            sentiment_counts.get('neutral', 0)
        ]

        colors = ['green', 'red', 'orange']

        plt.bar(labels, values, color=colors)

        plt.title("Sentiment Analysis")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")

        # Save image
        file_path = os.path.join(STATIC_FOLDER, "sentiment_chart.png")
        plt.savefig(file_path)
        plt.close()

        return file_path

    except Exception as e:
        print("Error in plot_sentiment_chart:", e)
        return None
   
