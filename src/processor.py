import pandas as pd
import requests

def process_repo_data(owner, repo, raw_data):
    commits_data = raw_data.get("commits")
    if not commits_data:
        return None
    commits_df = pd.DataFrame([
        {
            "date": c["commit"]["author"]["date"],
            "author": c["commit"]["author"]["name"]
        }
        for c in commits_data if c.get("commit")
    ])

    commits_df["date"] = pd.to_datetime(commits_df["date"])
    commits_df["week"] = commits_df["date"].dt.to_period("W").apply(lambda r: r.start_time)

    weekly_commits = commits_df.groupby("week").size().reset_index(name="commits")
    languages = raw_data.get("languages", {})
    pulls = len(raw_data.get("pulls", []))
    repo_info = raw_data.get("repo_info", {})
    contrib_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    contrib_response = requests.get(contrib_url).json()

    contrib_list = []
    if isinstance(contrib_response, list):
        for c in contrib_response:
            contrib_list.append({
                "author": c.get("login", "Unknown"),
                "commits": c.get("contributions", 0)
            })

    contributors_df = pd.DataFrame(contrib_list)

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    tree_response = requests.get(tree_url).json()

    file_rows = []
    if "tree" in tree_response:
        for item in tree_response["tree"]:
            if item["type"] == "blob":
                path = item["path"]
                ext = path.split(".")[-1] if "." in path else "no_ext"
                file_rows.append({"path": path, "extension": ext})

    files_df = pd.DataFrame(file_rows)

    return {
        "commits": weekly_commits,
        "languages": languages,
        "pulls": pulls,
        "stars": repo_info.get("stargazers_count", 0),
        "forks": repo_info.get("forks_count", 0),
        "watchers": repo_info.get("watchers_count", 0),
        "contributors": contributors_df,
        "files": files_df,
    }

