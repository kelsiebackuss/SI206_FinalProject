import sqlite3

conn = sqlite3.connect('mental_health_weather,db')
cur = conn.cursor()

# 1. Create the weather data table
cur.execute('''
CREATE TABLE IF NOT EXISTS WeatherData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    date TEXT,
    temperature REAL,
    humidity INTEGER,
    weather_condition TEXT,
    UNIQUE (city, date)
    );
    ''')

# 2. Create the Reddit keyword data table 
cur.execute('''
CREATE TABLE IF NOT EXISTS KeywordLookup (
    keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE
);
''')

# 3. Create the Reddit posts table
cur.execute('''
CREATE TABLE IF NOT EXISTS RedditPosts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER,
  city TEXT,
  data TEXT,
  title TEXT,
  score INTEGER,
  subreddit TEXT,
  FOREIGN KEY (keyword_id) REFERENCES KeywordLookup (keyword_id), 
  UNIQUE (title, data)
);
''')

conn.commit()
conn.close()
