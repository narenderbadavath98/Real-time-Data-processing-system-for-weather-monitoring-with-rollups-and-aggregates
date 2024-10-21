from flask import Flask, render_template, request
from visualizations.visualizations import (
    plot_daily_weather_summary,
    plot_historical_trends,
    plot_triggered_alerts
)
from real_time_bonus import get_detailed_weather_data
import os
import sys
import requests
import sqlite3
import pandas as pd
import time
import threading
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import logging
from email.mime.multipart import MIMEMultipart
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

API_KEY = '54016b09122721d79e651ea82f0a52fe'  # Replace with your own API key
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_historical_weather_data():
    # Load historical weather data
    return pd.read_csv('data/historical_weather_data.csv')

def get_daily_weather_summary(data):
    # Example of daily summary: you can customize this based on your data
    return data.groupby('date').agg({'temperature': 'mean', 'humidity': 'mean'}).reset_index()

def get_triggered_alerts(data):
    # Example of retrieving alerts (customize based on your alert logic)
    return data[data['alert_triggered'] == True]

def create_table():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            weather TEXT,
            temp REAL,
            feels_like REAL,
            timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table when the app starts
create_table()

def get_weather_data(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

def process_weather_data(data):
    if data:
        main_weather = data['weather'][0]['main']
        temp_kelvin = data['main']['temp']
        feels_like_kelvin = data['main']['feels_like']
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
        timestamp = data['dt']
        return {
            'weather': main_weather,
            'temp': round(temp_celsius, 2),
            'feels_like': round(feels_like_celsius, 2),
            'timestamp': timestamp
        }
    return None

# Store weather data in the database
def store_weather_data(city, data):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO weather_data (city, weather, temp, feels_like, timestamp) VALUES (?, ?, ?, ?, ?) ",
                  (city, data['weather'], data['temp'], data['feels_like'], data['timestamp']))
    conn.close()

# Calculate daily summary
def calculate_daily_summary(city):
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query(f"SELECT * FROM weather_data WHERE city='{city}'", conn)
    conn.close()
    if not df.empty:
        daily_summary = {
            'avg_temp': round(df['temp'].mean(), 2),
            'max_temp': df['temp'].max(),
            'min_temp': df['temp'].min(),
            'dominant_weather': df['weather'].mode()[0]  # Most frequent weather condition
        }
        return daily_summary
    else:
        return None

def update_weather_data():
    while True:
        cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
        for city in cities:
            data = get_weather_data(city)
            if data:
                processed_data = process_weather_data(data)
                store_weather_data(city, processed_data)
                logging.info(f"Updated weather data for {city}: {processed_data}")
        time.sleep(300)  # Sleep for 5 minutes

# Function to send email alerts
def send_email_alert(email, city, threshold_temp, current_temp):
    my_email = "iiitkottayamcoms@gmail.com"
    password = "qwyxksuejdmsglin"  # Be cautious with storing plain text passwords

    # Create the email message
    subject = f"Temperature Alert for {city}"
    body = (f"Alert: The temperature in {city} has exceeded your set threshold of {threshold_temp} °C! "
            f"Current temperature: {current_temp} °C.")

    # Create a MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = email
    msg['Subject'] = subject

    # Attach the body of the email with utf-8 encoding
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        # Set up the SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()  # Upgrade to a secure connection
            connection.login(user=my_email, password=password)  # Log in
            connection.sendmail(from_addr=my_email, to_addrs=email, msg=msg.as_string())  # Send email
            logging.info(f"Alert email sent to {email} for {city}.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")



@app.route('/')
def index():
    cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    weather_data = []

    # Fetch and process weather data for each city
    for city in cities:
        data = get_weather_data(city)
        if data:
            processed_data = process_weather_data(data)
            store_weather_data(city, processed_data)
            weather_data.append({
                'city': city,
                'weather': processed_data['weather'],
                'temp': processed_data['temp'],
                'feels_like': processed_data['feels_like'],
                'timestamp': datetime.utcfromtimestamp(processed_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            })

    # Get daily summary for one of the cities
    daily_summary = calculate_daily_summary('Delhi')

    # Get the last update time
    last_update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', weather_data=weather_data, daily_summary=daily_summary, last_update_time=last_update_time)

@app.route('/latest_weather', methods=['GET'])
def latest_weather():
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1", conn)
    conn.close()
    return df.to_json(orient='records')

def plot_triggered_alerts(weather_data):
    # Print the columns for debugging
    print("Available Columns in weather_data:")
    print(weather_data.columns.tolist())  # Print columns as a list for better visibility

    # Use 'alert_triggered' to filter for triggered alerts
    if 'alert_triggered' not in weather_data.columns:
        print("Column 'alert_triggered' not found in weather_data.")
        return

    # Filter based on 'alert_triggered' column
    triggered_alerts = weather_data[weather_data['alert_triggered'] == True]

    # Debugging output
    print("Triggered Alerts DataFrame:")
    print(triggered_alerts)

    if triggered_alerts.empty:
        print("No triggered alerts found.")
        return  # Exit if no alerts

    # Plotting alerts
    plt.figure(figsize=(10, 6))
    plt.plot(triggered_alerts['date'], triggered_alerts['alert_triggered'], marker='o', linestyle='-')
    plt.title('Triggered Alerts Over Time')
    plt.xlabel('Date')
    plt.ylabel('Alert Triggered')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()  # Display the plot

def load_weather_data(file_path='data/historical_weather_data.csv'):
    """
    Load weather data from a CSV file into a DataFrame.
    
    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the weather data.
    """
    try:
        # Read the CSV file into a DataFrame
        weather_data = pd.read_csv(file_path)
        print("Weather data loaded successfully.")
        return weather_data
    except Exception as e:
        print(f"Error loading weather data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
# Update the visualizations function to call the updated plot function
@app.route('/visualizations')
def visualizations():
    # Load your weather data here
    # Example:
    weather_data = load_weather_data()  # Ensure this function returns the correct DataFrame

    # Call the updated plot function
    plot_triggered_alerts(weather_data)

    return render_template('visualizations.html')






@app.route('/alert_registered', methods=['POST'])
def alert_registered():
    city = request.form['city']
    threshold_temp = float(request.form['threshold_temp'])
    email = request.form.get('email')  # Retrieve the user's email from the form

    # Check the latest weather data and trigger alerts
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query(f"SELECT * FROM weather_data WHERE city='{city}' ORDER BY timestamp DESC", conn)
    conn.close()

    alert_triggered = False
    current_temp = None  # Initialize current_temp

    # Check if there's any data for the specified city
    if not df.empty:
        # Get the most recent temperature
        current_temp = df['temp'].iloc[0]  # Get the latest temperature
        if current_temp > threshold_temp:
            alert_triggered = True
            
            # Send email alert
            send_email_alert(email, city, threshold_temp, current_temp)

    return render_template('alert_registered.html', alert_triggered=alert_triggered, city=city, threshold_temp=threshold_temp, current_temp=current_temp)
@app.route('/real_time_bonus', methods=['GET', 'POST'])
def real_time_bonus():
    weather_data = None  # Initialize weather_data
    if request.method == 'POST':
        city = request.form['city']  # Get city name from form
        # Fetch real-time weather data for the specified city
        weather_data = get_detailed_weather_data(city)
        
    return render_template('real_time_bonus.html', weather_data=weather_data)


if __name__ == '__main__':
    # Start the weather update thread
    update_thread = threading.Thread(target=update_weather_data)
    update_thread.daemon = True
    update_thread.start()
    
    app.run(debug=True)
