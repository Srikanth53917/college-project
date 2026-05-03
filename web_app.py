from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import traceback

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

            # Fetch data
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                result = {"error": "Invalid stock symbol"}
                return render_template("index.html", result=result)

            last_price = float(data["Close"].iloc[-1])

            # ML Prediction
            model = train_stock_model(data)
            predicted_price = predict_next_day(model, data)

            # Sentiment Analysis
            sentiment_score = analyze_sentiment_from_dataset(ticker)

            if sentiment_score > 0:
                sentiment = "Positive"
                recommendation = "Buy"
            elif sentiment_score < 0:
                sentiment = "Negative"
                recommendation = "Sell"
            else:
                sentiment = "Neutral"
                recommendation = "Hold"

            # Charts
            stock_chart = stock_price_chart(data, ticker)
            sentiment_img = sentiment_chart(sentiment_score)

            result = {
                "last_price": round(last_price, 2),
                "predicted_price": round(predicted_price, 2),
                "sentiment": sentiment,
                "recommendation": recommendation,
                "stock_chart": stock_chart,
                "sentiment_chart": sentiment_img
            }

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()
            result = {"error": "Something went wrong"}

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
