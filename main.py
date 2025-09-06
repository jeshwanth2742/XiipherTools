import tweepy
import os
from utils import get_start_time, filter_tweets_by_handle

# --- Setup X API client ---
bearer_token = os.environ.get("BEARER_TOKEN")  # Make sure to set this in your environment
client = tweepy.Client(bearer_token=bearer_token)

def get_user_id(x_handle: str) -> str:
    """
    Get the user ID for a given X handle.
    """
    user = client.get_user(username=x_handle)
    return user.data.id

def fetch_tweets(user_id: str, start_time):
    """
    Fetch tweets for a user since start_time.
    Returns a list of tweets.
    """
    tweets = client.get_users_tweets(
        id=user_id,
        start_time=start_time.isoformat("T") + "Z",
        tweet_fields=["public_metrics", "text"],
        max_results=100  # adjust or paginate if needed
    )
    return tweets.data or []

def calculate_metrics(tweets):
    """
    Aggregate engagement metrics from a list of tweets.
    Returns a dictionary with metrics.
    """
    metrics = {
        "Tweets": len(tweets),
        "Likes": sum(t.public_metrics['like_count'] for t in tweets),
        "Replies": sum(t.public_metrics['reply_count'] for t in tweets),
        "Retweets": sum(t.public_metrics['retweet_count'] for t in tweets),
        "Quotes": sum(t.public_metrics['quote_count'] for t in tweets)
    }
    return metrics
