import streamlit as st
from api_client import fetch_repo_data
from processor import process_repo_data
from viz import create_repo_visuals

st.set_page_config(page_title="GitMetric Dashboard", layout="wide")

st.title("GitMetric Dashboard")
st.sidebar.header("Repository Details")

username = st.sidebar.text_input("Enter GitHub Username", "")
repo_name = st.sidebar.text_input("Enter Repository Name", "")

if st.sidebar.button("Fetch Data"):
    if username and repo_name:
        with st.spinner("Fetching data from GitHub..."):
            raw_data = fetch_repo_data(username, repo_name)

            if raw_data:
                # FIX: pass owner + repo + raw_data
                processed_data = process_repo_data(username, repo_name, raw_data)

                if processed_data:
                    st.subheader(f"Repository: {username}/{repo_name}")
                    create_repo_visuals(processed_data)
                else:
                    st.warning("No commit data found. The repository may be empty, private, or GitHub hasn't generated commit stats yet.")
            else:
                st.error("Could not fetch data. Check repository name or try again.")
    else:
        st.warning("Please enter both username and repository name to continue.")

else:
    st.info("Enter a username and repository name, then click 'Fetch Data' to begin.")
