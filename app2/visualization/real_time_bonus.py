import requests
import logging

API_KEY = '54016b09122721d79e651ea82f0a52fe'  # Replace with your actual API key

def get_detailed_weather_data(city_name):
    """Fetch detailed weather data for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return process_weather_data(data)
    else:
        logging.error(f"Failed to get data for {city_name}: {response.status_code}")
        return None

def process_weather_data(data):
    """Process the fetched weather data and extract required metrics."""
    if data:
        city = data['name']
        temperatures = data['main']
        weather_conditions = data['weather'][0]
        
        avg_temp = temperatures['temp'] - 273.15  # Convert from Kelvin to Celsius
        max_temp = temperatures['temp_max'] - 273.15
        min_temp = temperatures['temp_min'] - 273.15
        humidity = temperatures['humidity']
        wind_speed = data['wind']['speed']
        
        # Determine the dominant weather condition
        dominant_condition = weather_conditions['main']
        condition_reason = weather_conditions['description']
        
        return {
            'city': city,
            'avg_temperature': round(avg_temp, 2),
            'max_temperature': round(max_temp, 2),
            'min_temperature': round(min_temp, 2),
            'humidity': humidity,
            'wind_speed': wind_speed,
            'dominant_condition': dominant_condition,
            'condition_reason': condition_reason
        }
    return None
