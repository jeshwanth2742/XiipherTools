from datetime import datetime, timedelta

def get_start_time(time_range: str):
    """Return UTC start time based on selected timeframe."""
    now = datetime.utcnow()
    delta_days = {"24h": 1, "7d": 7, "30d": 30, "90d": 90}.get(time_range, 1)
    return now - timedelta(days=delta_days)

def filter_tweets_by_handle(tweets, handle: str):
    """Return tweets that mention the given sub-project handle (@Anoma etc.)."""
    return [t for t in tweets if handle.lower() in t.text.lower()]
