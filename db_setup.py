import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('mental_health_weather.db')
cur = conn.cursor()

# TABLE 1: Weather data table
cur.execute('''
CREATE TABLE IF NOT EXISTS WeatherData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    date TEXT,
    temperature REAL,
    humidity INTEGER,
    weather_condition TEXT,
    UNIQUE(city, date)
);
''')

# TABLE 2: Keywords used to search Reddit
cur.execute('''
CREATE TABLE IF NOT EXISTS KeywordLookup (
    keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE
);
''')

# TABLE 3: Reddit posts matching those keywords
cur.execute('''
CREATE TABLE IF NOT EXISTS RedditPosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword_id INTEGER,
    city TEXT,
    date TEXT,
    title TEXT,
    score INTEGER,
    subreddit TEXT,
    FOREIGN KEY (keyword_id) REFERENCES KeywordLookup(keyword_id),
    UNIQUE(title, date)
);
''')

# Save changes and close connection
conn.commit()
conn.close()
