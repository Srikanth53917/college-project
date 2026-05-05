from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import traceback
import time

from prediction.stock_prediction import train_stock_model, predict_next_day
from sentiment.sentiment_analysis import analyze_sentiment_from_dataset
from visualization.charts import stock_price_chart, sentiment_chart

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            ticker = request.form.get("ticker").upper()
            start_year = int(request.form.get("start_year"))
            end_year = int(request.form.get("end_year"))

            start_date = f"{start_year}-01-01"
            end_date = f"{end_year}-12-31"

            # Delay to avoid rate limit
            time.sleep(3)

            # Fetch stock data
            data = yf.download(ticker, start=start_date, end=end_date)

            # Fix for yfinance MultiIndex columns (yfinance v0.2+)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            if data.empty:
                result = {"error": "Invalid stock symbol or no data available"}
                return render_template("index.html", result=result)

            # Last price
            try:
                last_price = float(data["Close"].iloc[-1])
                print("Last price fetched:", last_price)
            except Exception as e:
                print("Price fetch error:", e)
                last_price = 0

            # Prediction
            try:
                model, X_test, y_test = train_stock_model(data)
                last_close = float(data["Close"].iloc[-1])
                predicted_price = float(predict_next_day(model, last_close))
            except Exception as e:
                print("Prediction error:", e)
                predicted_price = last_price

            # Sentiment
            try:
                sentiment, scores = analyze_sentiment_from_dataset(start_year, end_year)
            except Exception as e:
                print("Sentiment error:", e)
                sentiment = "NEUTRAL"
                scores = {"positive": 1, "negative": 1, "neutral": 1}

            # Recommendation based on sentiment
            if sentiment == "POSITIVE":
                recommendation = "Buy"
                sentiment_class = "positive"
            elif sentiment == "NEGATIVE":
                recommendation = "Sell"
                sentiment_class = "negative"
            else:
                recommendation = "Hold"
                sentiment_class = "neutral"

            # Charts
            try:
                stock_price_chart(data)
                sentiment_chart(scores)
            except Exception as e:
                print("Chart error:", e)

            # Final result
            result = {
                "company": ticker,
                "last_price": round(last_price, 2),
                "predicted_price": round(predicted_price, 2),
                "sentiment": sentiment,
                "sentiment_class": sentiment_class,
                "decision": recommendation,
            }

        except Exception as e:
            print("MAIN ERROR:", e)
            traceback.print_exc()
            result = {"error": "Something went wrong. Try again."}

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
