import requests, sqlite3
from datetime import datetime

# 1. Define cities and keywords
cities = ["New York", "Berlin", "Paris", "Los Angeles"]
keywords = ["anxiety", "depression", "stress"]

# 2. Set up KeywordLookup table
def init_keywords():
    conn = sqlite3.connect("mental_health_weather.db")
    cur = conn.cursor()
    for word in keywords:
        cur.execute("INSERT OR IGNORE INTO KeywordLookup (keyword) VALUES (?)", (word,))
    conn.commit()
    conn.close()

# 3. Fetch posts from Reddit using JSON API
def get_posts(keyword, city, limit=25):
    url = f"https://www.reddit.com/search.json?q={keyword}%20{city}&limit=25&sort=new"
    headers = {"User-agent": "SI206ProjectBot"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching posts for keyword: {keyword}")
        return []
    return response.json()["data"]["children"]

# 4. Store posts in the database
def store_posts(keyword, city):
    conn = sqlite3.connect("mental_health_weather.db")
    cur = conn.cursor()

    # Get keyword_id from KeywordLookup
    cur.execute("SELECT keyword_id FROM KeywordLookup WHERE keyword=?", (keyword,))
    result = cur.fetchone()
    if not result:
        print(f"Keyword ID not found for {keyword}")
        conn.close()
        return
    keyword_id = result[0]

    posts = get_posts(keyword, city)
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

# Loop through cities + keywords
def run_reddit_collection():
    init_keywords()
    for city in cities:
        for kw in keywords:
            print(f"Fetching posts for '{kw}' in {city}...")
            store_posts(kw, city)

if __name__ == "__main__":
    run_reddit_collection()

