import sqlite3

# Connect to your database
conn = sqlite3.connect('mental_health_weather.db')
cur = conn.cursor()

# Fetch all table names
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

# Print results
print("Tables in your database:")
for table in tables:
    print(table[0])

conn.close()
