import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_from_dataset(ticker):
    try:
        # Load dataset
        df = pd.read_csv("sentiment/news_data.csv")

        # Filter rows containing ticker
        df = df[df["news"].str.contains(ticker, case=False, na=False)]

        if df.empty:
            return 0  # Neutral if no news found

        scores = []

        for news in df["news"]:
            score = analyzer.polarity_scores(news)["compound"]
            scores.append(score)

        avg_score = sum(scores) / len(scores)

        return avg_score

    except Exception as e:
        print("Sentiment error:", e)
        return 0
