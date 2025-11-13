from src.api_client import fetch_repo_data

def test_fetch_repo_data():
    data = fetch_repo_data("octocat", "Hello-World")
    assert "commits" in data
