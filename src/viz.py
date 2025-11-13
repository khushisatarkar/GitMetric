import streamlit as st
import plotly.express as px

def create_repo_visuals(processed_data):
    if not processed_data:
        st.warning("No data to visualize.")
        return

    commits_df = processed_data.get("commits")
    langs = processed_data.get("languages", {})
    pulls = processed_data.get("pulls", 0)

    if commits_df is not None:
        st.subheader("Commit Activity (Last 52 Weeks)")
        fig = px.line(commits_df, x="week", y="commits", title="Commits Over Time")
        st.plotly_chart(fig)
    else:
        st.info("No commit history available.")

    st.subheader("Language Usage")
    if langs:
        lang_fig = px.pie(names=list(langs.keys()), values=list(langs.values()), title="Language Breakdown")
        st.plotly_chart(lang_fig)
    else:
        st.info("No language data available.")

    st.metric("Total Pull Requests", pulls)
    st.metric("⭐ Stars", processed_data["stars"])
    st.metric("🍴 Forks", processed_data["forks"])
    st.metric("👀 Watchers", processed_data["watchers"])

