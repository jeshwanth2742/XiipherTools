import streamlit as st
from main import get_user_id, fetch_tweets, calculate_metrics
from utils import get_start_time, filter_tweets_by_handle

# --- Project / Sub-projects ---
main_project = "@KaitoAI"
sub_projects = ["@Anoma", "@Monad", "@Ethereum"]

st.title("KaitoAI Contribution Tracker (Basic Test)")

# 1️⃣ User Inputs
x_handle = st.text_input("Enter your X handle (@username)")
selected_sub_project = st.selectbox("Select sub-project", sub_projects)
time_range = st.selectbox("Select timeframe", ["24h", "7d", "30d", "90d"])

# 2️⃣ Fetch Contributions
if st.button("Fetch Contributions") and x_handle:

    try:
        # Get start time based on selected timeframe
        start_time = get_start_time(time_range)

        # Get user ID from handle
        user_id = get_user_id(x_handle)

        # Fetch tweets since start_time
        tweets = fetch_tweets(user_id, start_time)

        if not tweets:
            st.info("No tweets found for this timeframe.")
        else:
            # Filter tweets mentioning the selected sub-project (@handle)
            filtered = filter_tweets_by_handle(tweets, selected_sub_project)

            # Calculate engagement metrics
            metrics = calculate_metrics(filtered)

            # Display metrics
            st.subheader(f"Contribution Metrics for {x_handle} → {selected_sub_project} ({time_range})")
            st.write(metrics)

    except Exception as e:
        st.error(f"Error fetching data: {e}")

