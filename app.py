import streamlit as st
from main import get_user_id, fetch_tweets, calculate_metrics
from utils import get_start_time, filter_tweets_by_handle

# --- Project / Sub-projects ---
main_project = "@KaitoAI"
sub_projects = ["@Anoma", "@Monad", "@Ethereum"]

st.title("KaitoAI Contribution Tracker (Final)")

# 1️⃣ User Inputs
x_handle = st.text_input("Enter your X handle (@username)")
selected_sub_project = st.selectbox("Select sub-project", sub_projects)
time_range = st.selectbox("Select timeframe", ["24h", "7d", "30d", "90d"])

# 2️⃣ Fetch Contributions with caching
@st.cache_data(ttl=300)  # cache results for 5 minutes
def fetch_user_metrics(x_handle, sub_project, time_range):
    start_time = get_start_time(time_range)
    user_id = get_user_id(x_handle)
    tweets = fetch_tweets(user_id, start_time)
    filtered = filter_tweets_by_handle(tweets, sub_project)
    metrics = calculate_metrics(filtered)
    return metrics

if st.button("Fetch Contributions") and x_handle:
    try:
        metrics = fetch_user_metrics(x_handle, selected_sub_project, time_range)
        st.subheader(f"Contribution Metrics for {x_handle} → {selected_sub_project} ({time_range})")
        st.write(metrics)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

