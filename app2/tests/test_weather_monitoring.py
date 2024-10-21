import unittest
import sqlite3  # Add this line
from app import app, create_table, get_weather_data, process_weather_data, store_weather_data

class WeatherMonitoringTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up the test client
        cls.app = app.test_client()
        cls.app.testing = True
        # Create the database and the table for tests
        create_table()

    def test_get_weather_data_valid_city(self):
        city = "Delhi"
        response = get_weather_data(city)
        self.assertIsNotNone(response)
        self.assertIn('weather', response)
        self.assertIn('main', response)

    def test_get_weather_data_invalid_city(self):
        city = "InvalidCityName"
        response = get_weather_data(city)
        self.assertIsNone(response)

    def test_process_weather_data(self):
        mock_data = {
            'weather': [{'main': 'Clear'}],
            'main': {
                'temp': 298.15,
                'feels_like': 299.15
            },
            'dt': 1609459200  # Example timestamp
        }
        processed_data = process_weather_data(mock_data)
        self.assertIsNotNone(processed_data)
        self.assertEqual(processed_data['temp'], 25.0)  # 298.15 - 273.15
        self.assertEqual(processed_data['feels_like'], 26.0)  # 299.15 - 273.15

    def test_store_weather_data(self):
        mock_data = {
            'weather': 'Clear',
            'temp': 25.0,
            'feels_like': 26.0,
            'timestamp': 1609459200
        }
        store_weather_data("Delhi", mock_data)
        # Check if the data is stored in the database
        conn = sqlite3.connect('weather_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM weather_data WHERE city='Delhi'")
        data = c.fetchall()
        conn.close()
        self.assertGreater(len(data), 0)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather', response.data)  # Check if 'Weather' is in the response

if __name__ == '__main__':
    unittest.main()
