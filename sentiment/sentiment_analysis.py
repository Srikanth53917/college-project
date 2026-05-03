import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_from_dataset(ticker):
    try:
        # Load dataset
        df = pd.read_csv("sentiment/news_data.csv")

        # Ensure column exists
        if "news" not in df.columns:
            print("Column 'news' not found")
            return 0

        # Filter news related to ticker
        filtered = df[df["news"].str.contains(ticker, case=False, na=False)]

        # If no matching news → use full dataset
        if filtered.empty:
            filtered = df

        scores = []

        for news in filtered["news"]:
            score = analyzer.polarity_scores(str(news))["compound"]
            scores.append(score)

        # Calculate average sentiment
        avg_score = sum(scores) / len(scores)

        return avg_score

    except Exception as e:
        print("Sentiment Error:", e)
        return 0
