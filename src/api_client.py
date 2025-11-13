import requests

def fetch_repo_data(username, repo_name):
    base_url = f"https://api.github.com/repos/{username}/{repo_name}"
    stats_endpoints = {
        "commits": f"{base_url}/commits?per_page=100",
        "languages": f"{base_url}/languages",
        "pulls": f"{base_url}/pulls?state=all",
        "repo_info": base_url
    }

    data = {}
    for key, url in stats_endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            data[key] = response.json()
        else:
            data[key] = None
    return data