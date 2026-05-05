from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import time

from visualization.charts import plot_stock_chart, plot_sentiment_chart

app = Flask(__name__)


# Dummy sentiment (simple working logic)
def analyze_sentiment():
    return {
        "positive": 5,
        "negative": 2,
        "neutral": 3
    }


@app.route("/", methods=["GET", "POST"])
def home():
    stock_chart = None
    sentiment_chart = None
    result = None

    if request.method == "POST":
        try:
            ticker = request.form["ticker"].upper()
            start_year = int(request.form["start_year"])
            end_year = int(request.form["end_year"])

            start = f"{start_year}-01-01"
            end = f"{end_year}-12-31"

            # 🔥 Fetch stock data
            data = yf.download(ticker, start=start, end=end)

            if data.empty:
                return render_template("index.html", error="No data found")

            # Last price
            last_price = round(data['Close'].iloc[-1], 2)

            # Simple prediction (demo)
            predicted_price = round(last_price * 1.02, 2)

            # Sentiment
            sentiment_counts = analyze_sentiment()

            # Charts
            stock_chart = plot_stock_chart(data)
            sentiment_chart = plot_sentiment_chart(sentiment_counts)

            # Decision
            decision = "Buy" if sentiment_counts["positive"] > sentiment_counts["negative"] else "Hold"

            result = {
                "company": ticker,
                "last_price": last_price,
                "predicted_price": predicted_price,
                "sentiment": "Mixed",
                "decision": decision
            }

        except Exception as e:
            print("ERROR:", e)

    return render_template("index.html",
                           result=result,
                           stock_chart=stock_chart,
                           sentiment_chart=sentiment_chart)


if __name__ == "__main__":
    app.run(debug=True)
