# 1. necessary imports 
import requests, sqlite3
from datetime import datetime

# 2. Define keywords we will be analyzing via Reddit 
keywords = ["anxiety", "depression", "stress"]
city = "Ann Arbor" # UPDATE THIS TO ACCOUNT FOR ALL CITIES WE ARE ANALYZING 

def init_keywords():
  conn = sqlite3.connect('mental_health_weather.db')
  cur = conn.cursor()
  for word in keywords:
    cur.execute("INSERT OR IGNOTE INTO KeywordLookup (keyword) VALUES (?)", (word,))
  conn.commit()
  conn.close()

# 3. Pull posts from Reddit API
def get_posts(keyword, limit=25):
  url = "https://api.pushshift.io/reddit/search/submission/"
  params = {
    "q": keyword,
    "size": limit,
    "sort": "desc"
  }
  response = requests.get(url, params=params)
  return response.json()["data"]

# 4. Store pulled posts into a database
def store_posts(keyword):
  conn = sqlite3.connect('mental_health_weather.db')
  cur = conn.cursor()

  # Acquire keyword_id to use as foreign key
