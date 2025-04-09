import requests
import sqlite3
import datetime

API_KEY = "KKfuINNnA0noEVntHneY3uAkGQ8J96aC"  # Your actual API key

def get_top_cities(number=50):
    """Fetches the top cities from AccuWeather API."""
    url = f"http://dataservice.accuweather.com/locations/v1/topcities/{number}"  # Use the number parameter here
    params = {
        'apikey': API_KEY,  # The API key is used here to authenticate your request
        'language': 'en-us',
        'details': 'false'
    }

    try:
        response = requests.get(url, params=params)  # Sends the request

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Returns the data as JSON
        else:
            print(f"Error: Unable to fetch top cities data. Status code {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    top_cities = get_top_cities(50)  # Fetch top 50 cities
    if top_cities:
        print("Top Cities List:")
        for city in top_cities:
            # Printing city names and country names
            print(f"{city['LocalizedName']}, {city['Country']['EnglishName']}")

if __name__ == "__main__":
    main()
