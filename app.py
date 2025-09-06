import streamlit as st
import tweepy
from datetime import datetime, timedelta

# --- X API Setup ---
bearer_token = "YOUR_BEARER_TOKEN"  # replace with your token
client = tweepy.Client(bearer_token=bearer_token)

# --- Project & Sub-project Mapping ---
project_mapping = {
    "Kaito AI": ["@Anoma", "@NodePay", "@SparkLite"],
    "Cookie": ["@MindIO", "@Wallchain"]
}

# --- Streamlit UI ---
st.title("Web3 Project Contribution Tracker")

# User inputs
x_handle = st.text_input("Enter your X handle (@username)")
main_project = st.selectbox("Select main project", list(project_mapping.keys()))
sub_projects = st.multiselect("Select sub-project(s)", project_mapping[main_project])
time_range = st.selectbox("Select timeframe", ["24h", "7d", "30d", "90d"])

if st.button("Check Contributions") and x_handle:

    # Calculate start_time based on selected timeframe
    now = datetime.utcnow()
    if time_range == "24h":
        start_time = now - timedelta(days=1)
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
    elif time_range == "30d":
        start_time = now - timedelta(days=30)
    else:  # 90d
        start_time = now - timedelta(days=90)

    try:
        # Get user ID
        user = client.get_user(username=x_handle)
        user_id = user.data.id

        # Fetch tweets in timeframe
        tweets = client.get_users_tweets(
            id=user_id,
            start_time=start_time.isoformat("T") + "Z",
            tweet_fields=["public_metrics", "created_at", "text"],
            max_results=100  # paginate if needed
        )

        if not tweets.data:
            st.info("No tweets found in this period.")
        else:
            # Filter tweets for each selected sub-project
            all_metrics = {}
            for sub_proj in sub_projects:
                filtered = [
                    t for t in tweets.data
                    if sub_proj.lower() in t.text.lower()
                ]
                total_likes = sum(t.public_metrics['like_count'] for t in filtered)
                total_replies = sum(t.public_metrics['reply_count'] for t in filtered)
                total_retweets = sum(t.public_metrics['retweet_count'] for t in filtered)
                total_quotes = sum(t.public_metrics['quote_count'] for t in filtered)

                all_metrics[sub_proj] = {
                    "Tweets": len(filtered),
                    "Likes": total_likes,
                    "Replies": total_replies,
                    "Retweets": total_retweets,
                    "Quotes": total_quotes
                }

            # Display metrics
            st.subheader(f"Contribution Metrics for {x_handle} ({time_range})")
            for sub_proj, metrics in all_metrics.items():
                st.markdown(f"### {sub_proj}")
                st.write(metrics)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
