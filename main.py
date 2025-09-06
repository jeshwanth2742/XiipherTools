import tweepy
from utils import filter_tweets_by_handle

# Load bearer token from Streamlit secrets or environment
import streamlit as st
bearer_token = st.secrets["BEARER_TOKEN"]

# Setup Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

def get_user_id(x_handle: str) -> str:
    """Get X user ID from handle."""
    user = client.get_user(username=x_handle)
    return user.data.id

def fetch_tweets(user_id: str, start_time):
    """Fetch tweets for a user since start_time."""
    tweets = client.get_users_tweets(
        id=user_id,
        start_time=start_time.isoformat("T")+"Z",
        tweet_fields=["public_metrics", "text"],
        max_results=100
    )
    return tweets.data or []

def calculate_metrics(tweets):
    """Aggregate engagement metrics."""
    metrics = {
        "Tweets": len(tweets),
        "Likes": sum(t.public_metrics['like_count'] for t in tweets),
        "Replies": sum(t.public_metrics['reply_count'] for t in tweets),
        "Retweets": sum(t.public_metrics['retweet_count'] for t in tweets),
        "Quotes": sum(t.public_metrics['quote_count'] for t in tweets)
    }
    return metrics
