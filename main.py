import tweepy
import streamlit as st
from utils import filter_tweets_by_handle
from tweepy.errors import TooManyRequests
import time

# Load bearer token from Streamlit Secrets
bearer_token = st.secrets["BEARER_TOKEN"]

# Setup Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

def get_user_id(x_handle: str) -> str:
    """Get X user ID from handle."""
    user = client.get_user(username=x_handle)
    return user.data.id

def format_rfc3339(dt):
    """Return RFC3339 datetime string without microseconds."""
    return dt.replace(microsecond=0).isoformat("T") + "Z"

def fetch_tweets(user_id: str, start_time):
    """Fetch tweets for a user since start_time, handle rate limits."""
    start_time_str = format_rfc3339(start_time)
    while True:
        try:
            tweets = client.get_users_tweets(
                id=user_id,
                start_time=start_time_str,
                tweet_fields=["public_metrics", "text"],
                max_results=100
            )
            return tweets.data or []
        except TooManyRequests:
            st.warning("Rate limit reached. Waiting 60 seconds...")
            time.sleep(60)  # wait and retry

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

