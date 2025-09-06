from datetime import datetime, timedelta

def get_start_time(time_range: str) -> datetime:
    """
    Return the UTC start time based on the selected timeframe.
    
    Args:
        time_range (str): "24h", "7d", "30d", or "90d"
    
    Returns:
        datetime: UTC datetime for start of timeframe
    """
    now = datetime.utcnow()
    delta_days = {"24h": 1, "7d": 7, "30d": 30, "90d": 90}.get(time_range, 1)
    return now - timedelta(days=delta_days)

def filter_tweets_by_handle(tweets, handle: str):
    """
    Filter a list of tweets to only include tweets that mention a given sub-project handle.
    
    Args:
        tweets (list): List of tweet objects
        handle (str): Sub-project handle (e.g., "@Anoma")
    
    Returns:
        list: Filtered list of tweets mentioning the handle
    """
    return [t for t in tweets if handle.lower() in t.text.lower()]
