from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import time
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
            print("🔥 Request received")

            ticker = request.form["ticker"].upper()
            start_year = int(request.form["start_year"])
            end_year = int(request.form["end_year"])

            start_date = f"{start_year}-01-01"
            end_date = f"{end_year}-12-31"

            print("📥 Fetching stock data...")
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                print("❌ No stock data")
                return render_template("index.html", result=None)

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data = data.dropna()

            stock = yf.Ticker(ticker)
            company_name = stock.info.get("longName", ticker)

            print("🤖 Training model...")
            model, _, _ = train_stock_model(data)

            last_close = float(data['Close'].iloc[-1])
            predicted_price = float(predict_next_day(model, last_close))

            print("🧠 Running sentiment...")
            sentiment, scores = analyze_sentiment_from_dataset(start_year, end_year)

            print("📊 Generating charts...")
            stock_price_chart(data)
            sentiment_chart(scores)

            if sentiment == "POSITIVE":
                sentiment_class = "positive"
            elif sentiment == "NEGATIVE":
                sentiment_class = "negative"
            else:
                sentiment_class = "neutral"

            if predicted_price > last_close and sentiment == "POSITIVE":
                decision = "STRONG BUY"
            elif predicted_price < last_close and sentiment == "NEGATIVE":
                decision = "SELL"
            else:
                decision = "HOLD"

            result = {
                "company": f"{company_name} ({ticker})",
                "last_price": round(last_close, 2),
                "predicted_price": round(predicted_price, 2),
                "sentiment": sentiment,
                "sentiment_class": sentiment_class,
                "decision": decision
            }

        except Exception as e:
            print("🚨 ERROR:", e)
            return f"<h2>Error: {e}</h2>"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
