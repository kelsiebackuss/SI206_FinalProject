import requests, sqlite3
from datetime import datetime

# Keywords to track
keywords = ["anxiety", "depression", "stress"]
city = "Ann Arbor"

# Set up KeywordLookup table
def init_keywords():
    conn = sqlite3.connect("mental_health_weather.db")
    cur = conn.cursor()
    for word in keywords:
        cur.execute("INSERT OR IGNORE INTO KeywordLookup (keyword) VALUES (?)", (word,))
    conn.commit()
    conn.close()

# Pull posts from Reddit’s public JSON API
def get_posts(keyword, limit=25):
    url = f"https://www.reddit.com/search.json?q={keyword}&limit={limit}&sort=new"
    headers = {"User-agent": "SI206ProjectBot"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data for {keyword}")
        return []
    return response.json()["data"]["children"]

# Store Reddit posts into database
def store_posts(keyword):
    conn = sqlite3.connect("mental_health_weather.db")
    cur = conn.cursor()

    # Get keyword_id from lookup table
    cur.execute("SELECT keyword_id FROM KeywordLookup WHERE keyword=?", (keyword,))
    keyword_id = cur.fetchone()[0]

    posts = get_posts(keyword)
    for post in posts:
        data = post["data"]
        title = data.get("title", "")
        score = data.get("score", 0)
        subreddit = data.get("subreddit", "unknown")
        utc_time = data.get("created_utc")
        if utc_time:
            date = datetime.utcfromtimestamp(utc_time).strftime("%Y-%m-%d")
        else:
            date = "unknown"

        try:
            cur.execute("""
                INSERT OR IGNORE INTO RedditPosts (keyword_id, city, date, title, score, subreddit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (keyword_id, city, date, title, score, subreddit))
        except:
            continue

    conn.commit()
    conn.close()

# Run all
def run_reddit_collection():
    init_keywords()
    for kw in keywords:
        store_posts(kw)

if __name__ == "__main__":
    run_reddit_collection()
