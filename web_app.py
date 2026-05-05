from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import traceback
import time

from prediction.stock_prediction import train_stock_model, predict_next_day
from sentiment.sentiment_analysis import analyze_sentiment_from_dataset

from visualization.charts import plot_stock_chart, plot_sentiment_chart

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

            # 🔥 IMPORTANT: Delay to avoid rate limit
            time.sleep(3)

            # 📊 Fetch stock data
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                result = {"error": "Invalid stock symbol or no data available"}
                return render_template("index.html", result=result)

            # 💰 Last price
            try:
                last_price = float(data["Close"].iloc[-1])
            except:
                last_price = 0

            # 🤖 Prediction
            try:
                model = train_stock_model(data)
                predicted_price = float(predict_next_day(model, data))
            except Exception as e:
                print("Prediction error:", e)
                predicted_price = last_price

            # 🧠 Sentiment
            try:
                sentiment_score = analyze_sentiment_from_dataset(start_year,end_year)
            except Exception as e:
                print("Sentiment error:", e)
                sentiment_score = 0

            # 📊 Sentiment logic
            if sentiment_score > 0:
                sentiment = "Positive"
                recommendation = "Buy"
            elif sentiment_score < 0:
                sentiment = "Negative"
                recommendation = "Sell"
            else:
                sentiment = "Neutral"
                recommendation = "Hold"

            # 📈 Charts
            try:
                stock_chart = plot_stock_chart(data, ticker)
                sentiment_img = plot_sentiment_chart(sentiment_counts)
            except Exception as e:
                print("Chart error:", e)
                stock_chart = None
                sentiment_img = None

            # ✅ FINAL RESULT
            result = {
                "company": ticker,
                "last_price": round(last_price, 2),
                "predicted_price": round(predicted_price, 2),
                "sentiment": sentiment,
                "recommendation": recommendation,
                "stock_chart": stock_chart,
                "sentiment_chart": sentiment_img
            }

        except Exception as e:
            print("MAIN ERROR:", e)
            traceback.print_exc()
            result = {"error": "Something went wrong. Try again."}

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
