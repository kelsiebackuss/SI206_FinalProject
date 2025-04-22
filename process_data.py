import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mental_health_weather.db")
cur = conn.cursor()

# Drop old table if needed (optional for testing)
cur.execute("DROP TABLE IF EXISTS JoinedData")

# 1. Create a new JoinedData table
cur.execute('''
    CREATE TABLE IF NOT EXISTS JoinedData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        uv REAL,
        uv_max REAL,
        ozone REAL,
        post_title TEXT,
        score INTEGER,
        keyword_id INTEGER,
        subreddit TEXT
    )
''')

# 2. Populate the JoinedData table from RedditPosts and UVData
cur.execute('''
    INSERT INTO JoinedData (city, date, uv, uv_max, ozone, post_title, score, keyword_id, subreddit)
    SELECT 
        r.city,
        r.date,
        u.uv,
        u.uv_max,
        u.ozone,
        r.title,
        r.score,
        r.keyword_id,
        r.subreddit
    FROM RedditPosts r
    JOIN UVData u ON r.city = u.city AND r.date = u.date
''')

conn.commit()

# 3. Load data into pandas for analysis
df = pd.read_sql_query("SELECT * FROM JoinedData", conn)

# 4. Bin UV into categories
df["uv_range"] = pd.cut(
    df["uv"],
    bins=[-1, 2, 5, 7, 10],
    labels=["Low", "Moderate", "High", "Very High"]
)

# 5. Calculate average Reddit score per UV level
avg_score_by_uv = df.groupby("uv_range")["score"].mean().round(2)

# 6. Count Reddit posts per UV level
post_counts_by_uv = df["uv_range"].value_counts()

# 7. Export to files
avg_score_by_uv.to_csv("avg_score_by_uv.csv")
post_counts_by_uv.to_csv("post_counts_by_uv.csv")
avg_score_by_uv.to_json("avg_score_by_uv.json")
post_counts_by_uv.to_json("post_counts_by_uv.json")

# Close connection
conn.close()

# Print summary
print(" JoinedData created.")
print(" Averages and counts exported.")
