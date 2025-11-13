import pandas as pd

def process_repo_data(data):
    commits_data = data.get("commits")
    if not commits_data:
        return None

    # extracting commit dates and authors
    commits_df = pd.DataFrame([
        {
            "date": c["commit"]["author"]["date"],
            "author": c["commit"]["author"]["name"]
        }
        for c in commits_data if c.get("commit")
    ])
    commits_df["date"] = pd.to_datetime(commits_df["date"])
    commits_df["week"] = commits_df["date"].dt.to_period("W").apply(lambda r: r.start_time)

    # get weekly commit counts
    weekly_commits = commits_df.groupby("week").size().reset_index(name="commits")

    languages = data.get("languages", {})
    pulls = len(data.get("pulls", []))
    repo_info = data.get("repo_info", {})

    return {
        "commits": weekly_commits,
        "languages": languages,
        "pulls": pulls,
        "stars": repo_info.get("stargazers_count", 0),
        "forks": repo_info.get("forks_count", 0),
        "watchers": repo_info.get("watchers_count", 0)
    }
