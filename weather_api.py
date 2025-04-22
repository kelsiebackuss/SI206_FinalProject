import requests, sqlite3
from datetime import datetime, timedelta
from config import OPENUV_API_KEY

DB_NAME = "mental_health_weather.db"

cities = {
    "Berlin": (52.52, 13.405),
    "Paris": (48.8566, 2.3522),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437)
}

def get_uv_data(city, lat, lng):
    url = "https://api.openuv.io/api/v1/uv"
    headers = {"x-access-token": OPENUV_API_KEY}
    params = {
        "lat": lat,
        "lng": lng
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f" Error fetching UV data for {city}")
        return None

    data = response.json()
    return {
        "city": city,
        "date": data["result"]["uv_time"].split("T")[0],
        "uv": data["result"]["uv"],
        "uv_max": data["result"]["uv_max"],
        "ozone": data["result"].get("ozone", None)
    }

def store_uv_data(city, date, uv, uv_max, ozone):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS UVData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            uv REAL,
            uv_max REAL,
            ozone REAL,
            UNIQUE(city, date)
        )
    ''')
    cur.execute('''
        INSERT OR IGNORE INTO UVData (city, date, uv, uv_max, ozone)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, date, uv, uv_max, ozone))
    conn.commit()
    conn.close()

def run_uv_collection():
    count = 0
    max_rows = 100  # goal for the rubric
    total_days_back = 40  # check up to 40 days to get enough unique entries

    for i in range(total_days_back):
        if count >= max_rows:
            print(" 100 rows collected.")
            return
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        for city, (lat, lng) in cities.items():
            if count >= max_rows:
                break
            url = f"https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}&dt={date}T12:00:00Z"
            headers = {"x-access-token": OPENUV_API_KEY}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f" Skipping {city} on {date} — Status: {response.status_code}")
                continue
            try:
                data = response.json()["result"]
                store_uv_data(
                    city,
                    date,
                    data["uv"],
                    data["uv_max"],
                    data.get("ozone", None)
                )
                print(f"Added {city} on {date} — UV: {data['uv']}")
                count += 1
            except Exception as e:
                print(f" Error parsing {city} on {date}: {e}")

    print(f" Finished early — only {count} rows inserted (try increasing total_days_back)")

if __name__ == "__main__":
    run_uv_collection()
