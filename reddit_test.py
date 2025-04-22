import requests

def fetch_reddit_posts(keyword, limit=5):
    url = f"https://www.reddit.com/search.json?q={keyword}&limit={limit}&sort=new"
    headers = {"User-agent": "SI206ProjectBot"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        posts = response.json()["data"]["children"]
        for post in posts:
            title = post["data"]["title"]
            subreddit = post["data"]["subreddit"]
            score = post["data"]["score"]
            print(f"{title} — r/{subreddit} ({score} points)")
    else:
        print("❌ Reddit request failed with status:", response.status_code)

# Run it
fetch_reddit_posts("anxiety", limit=5)
