import streamlit as st
import plotly.express as px

def create_repo_visuals(processed_data):
    if not processed_data:
        st.warning("No data to visualize.")
        return

    st.markdown("---")

    commits_df = processed_data.get("commits")
    langs = processed_data.get("languages", {})
    pulls = processed_data.get("pulls", 0)
    stars = processed_data.get("stars", 0)
    forks = processed_data.get("forks", 0)
    watchers = processed_data.get("watchers", 0)

    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.subheader("Commit Activity (Last 52 Weeks)")

            if commits_df is not None and not commits_df.empty:
                fig = px.line(
                    commits_df,
                    x="week",
                    y="commits",
                    title="Commits Over Time"
                )
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No commit history available.")

        with col2:
            st.subheader("Language Usage")
            if langs:
                lang_fig = px.pie(
                    names=list(langs.keys()),
                    values=list(langs.values()),
                    title="Language Breakdown"
                )
                lang_fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(lang_fig, use_container_width=True)
            else:
                st.info("No language data available.")

    st.markdown("---")

    metric_cols = st.columns([1, 1, 1, 1])
    metric_cols[0].metric("Stars", stars)
    metric_cols[1].metric("Forks", forks)
    metric_cols[2].metric("Watchers", watchers)
    metric_cols[3].metric("Pull Requests", pulls)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("Contributor Insights")

    col5, col6 = st.columns([1, 1], gap="large")
    with col5:
        st.subheader("Top Contributors")
        if commits_df is not None and "author" in commits_df.columns:
            contributor_df = commits_df["author"].value_counts().reset_index()
            contributor_df.columns = ["author", "commits"]

            contrib_fig = px.bar(
                contributor_df,
                x="author",
                y="commits",
                title="Commits per Contributor"
            )
            contrib_fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(contrib_fig, use_container_width=True)
        else:
            st.info("No contributor data available.")

    with col6:
        st.subheader("File Type Distribution")
        files_df = processed_data.get("files")

        if files_df is not None and "extension" in files_df.columns:
            ext_counts = files_df["extension"].value_counts().reset_index()
            ext_counts.columns = ["extension", "count"]

            ext_fig = px.pie(
                ext_counts,
                names="extension",
                values="count",
                title="File Extension Breakdown"
            )
            ext_fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(ext_fig, use_container_width=True)
        else:
            st.info("No file extension data available.")
