import requests
import sqlite3
import datetime

# Set your OpenWeatherMap API Key here
API_KEY = "YOUR_API_KEY"

def get_weather_data(city):
    """
    Fetches weather data from OpenWeatherMap API for the given city.

    Args:
    city (str): Name of the city to fetch weather data for.

    Returns:
    dict: The weather data for the city.
    """
    # URL to call the weather API for current weather conditions
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    # Make the GET request to fetch weather data
    response = requests.get(url)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON data returned by the API
        return data
    else:
        print(f"Error: Unable to retrieve data for {city}.")
        return None

def store_weather_data(city, weather_data):
    """
    Stores the weather data into the SQLite database.

    Args:
    city (str): The name of the city for which the data is fetched.
    weather_data (dict): The weather data dictionary containing the weather details.
    """
    # Extract relevant weather data
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    weather_condition = weather_data['weather'][0]['description']
    date = datetime.datetime.now().strftime('%Y-%m-%d')  # Get the current date

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('mental_health_weather.db')
    cursor = conn.cursor()

    # Create the weather_data table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                        id INTEGER PRIMARY KEY,
                        city TEXT,
                        date TEXT,
                        temperature REAL,
                        humidity INTEGER,
                        weather_condition TEXT)''')
    
    # Insert the weather data into the table
    cursor.execute('''INSERT OR IGNORE INTO weather_data 
                      (city, date, temperature, humidity, weather_condition) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (city, date, temperature, humidity, weather_condition))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main():
    """
    Main function to fetch weather data for a list of cities and store them in the database.
    """
    cities = ["Ann Arbor", "Detroit", "Chicago"]  # List of cities to fetch weather data for

    for city in cities:
        weather_data = get_weather_data(city)  # Get the weather data
        if weather_data:  # If weather data is available
            store_weather_data(city, weather_data)  # Store the data in the database

# Call the main function to execute the script
if __name__ == "__main__":
    main()

