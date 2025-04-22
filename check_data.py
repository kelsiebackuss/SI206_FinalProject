import sqlite3

conn = sqlite3.connect("mental_health_weather.db")
cur = conn.cursor()

print("\nPreview of RedditPosts:")
cur.execute("SELECT city, date, title, score, subreddit FROM RedditPosts ORDER BY city, date LIMIT 20")
rows = cur.fetchall()
for row in rows:
    print(row)

print("\nCities in RedditPosts:")
cur.execute("SELECT DISTINCT city FROM RedditPosts")
cities = cur.fetchall()
for city in cities:
    print("-", city[0])

conn.close()
