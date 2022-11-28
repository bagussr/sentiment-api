from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import tweepy
import pandas as pd


class Sentiment:
    def __init__(self):
        self.consumer_key = "earScsYmfXq5tOUpzEziXxKwt"
        self.consumer_secret = "C6VouJVg0UUahbSqasFQAcRUE3dNdnaZFamS9zrXnp4cqOvAyP"
        self.access_token = "66106451-UFbSuHUjKFViuD5RaW3B14AIMmzlEcuEMFK4xrZCu"
        self.access_token_secret = "xw78fGFsSmdX3KXZpHIgcU03yK64gxoYfZ2lfjhyZ5stU"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.api = tweepy.API(self.auth)
        self.tweets = []
        self.pd = None

    def crawler(self, keyword, limit=200):
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        tweets = tweepy.Cursor(
            self.api.search_tweets, q=keyword + "-filter:retweets", lang="id", tweet_mode="extended"
        ).items(limit)
        for tweet in tweets:
            self.tweets.append(tweet.full_text)
        self.pd = pd.DataFrame(self.tweets, columns=["tweet"])

    def create_wordcloud(self, path, data):
        stopwords = set(STOPWORDS)
        wc = WordCloud(
            background_color="white",
            # mask = mask,
            max_words=100,
            stopwords=stopwords,
            repeat=True,
        )
        wc.generate(data.str.cat(sep=" "))
        wc.to_file(f"public/{path}.png")

    def getSentiment(self, title):
        self.pd["subjectivity"] = self.pd["tweet"].apply(self.getSubjectivity)
        self.pd["polarity"] = self.pd["tweet"].apply(self.getPolarity)
        self.pd["sentiment"] = self.pd["polarity"].apply(self.analyze)
        self.create_wordcloud(f"{title}_positive", self.pd["tweet"].loc[self.pd["sentiment"] == "positif"])
        self.create_wordcloud(f"{title}_negative", self.pd["tweet"].loc[self.pd["sentiment"] == "negatif"])
        self.create_wordcloud(f"{title}", self.pd["tweet"])

    @staticmethod
    def getSubjectivity(review):
        return TextBlob(review).sentiment.subjectivity

    @staticmethod
    def getPolarity(review):
        return TextBlob(review).sentiment.polarity

    @staticmethod
    def analyze(score):
        if score < 0:
            return "negatif"
        elif score == 0:
            return "netral"
        else:
            return "positif"
