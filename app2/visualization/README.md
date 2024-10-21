# Real-Time Data Processing System for Weather Monitoring
## Table of Contents
1. [Overview](#overview)
2. [Objective](#objective)
3. [Features](#features)
4. [Application Structure](#application-structure)
5. [Installation](#installation)
   - [Clone the Repository](#clone-the-repository)
   - [Create a Virtual Environment](#create-a-virtual-environment)
   - [Activate the Virtual Environment](#activate-the-virtual-environment)
   - [Install Dependencies](#install-dependencies)
6. [API Key](#api-key)
7. [Running the Application](#running-the-application)
8. [Navbar Explanation](#navbar-explanation)
9. [Bonus Features](#bonus-features)
10. [Test Cases](#test-cases)

## Overview
This project is a Real-Time Data Processing System designed to monitor weather conditions and provide summarized insights using rollups and aggregates. It utilizes data from the [OpenWeatherMap API](https://openweathermap.org/) to retrieve and process real-time weather information for major metros in India.

## Objective
The objective of this application is to continuously retrieve weather data and calculate daily weather summaries, implement alerting thresholds, and provide visualizations of the data.

## Features
- **Real-Time Weather Data Retrieval**: The application retrieves weather data every 5 minutes for the following cities:
  - Delhi
  - Mumbai
  - Chennai
  - Bangalore
  - Kolkata
  - Hyderabad

- **Data Processing**:
  - Converts temperature values from Kelvin to Celsius.
  - Generates daily weather summaries, including:
    - Average temperature
    - Maximum temperature
    - Minimum temperature
    - Dominant weather condition

- **Alerting System**: Configurable thresholds for temperature or specific weather conditions to trigger alerts.

- **Visualizations**: Displays daily weather summaries, historical trends, and alerts.

## Application Structure
- **`app.py`**: Main application file that handles routes and data processing.
- **`real_time_bonus.py`**: Contains functions to retrieve detailed weather data.
- **`visualizations/visualizations.py`**: Contains functions for generating various visualizations.
- **`data/`**: Directory for storing historical weather data.
- **`static/`**: Directory for CSS and JavaScript files.
- **`templates/`**: Contains HTML files for rendering web pages.

## Installation

###  1. Clone the Repository
```bash
git clone https://github.com/AkshayReddyy16/Rule-Engine-with-AST.git
cd Rule-Engine-with-AST
```
###  2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate      # For Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## API Key
To use the OpenWeatherMap API, you need to sign up for a free API key:

1. Go to [OpenWeatherMap](https://openweathermap.org/).
2. Create an account and obtain your API key.
3. Store the API key in a secure location and use it in the application.

## Running the Application

1. Ensure you have the required dependencies installed.
2. Set your API key in the application code or in an environment variable.
3. Run the application using the command:
   ```bash
   python app.py
   ```
   The application will start, and you can access it in your web browser at http://localhost:5000.
# Navbar Explanation

The navbar provides easy navigation throughout the application:

- **Home**: Redirects to the main dashboard.
- **Live Weather**: Displays real-time weather updates.
- **Summary**: Shows the daily weather summary.
- **Visualization**: Provides visual representations of the weather data.
- **Feedback**: Section for user feedback.
# Bonus Features

- **Historical Data**: Extend the application to support additional weather parameters (e.g., humidity, wind speed) and incorporate them into rollups and aggregates.
- **Forecast Retrieval**: Implement functionality to retrieve weather forecasts and generate summaries based on predicted conditions.
# Test Cases

- **System Setup**: Ensure the system starts successfully and connects to the OpenWeatherMap API using a valid API key.
- **Data Retrieval**: Simulate API calls at configurable intervals and ensure the system retrieves and parses weather data correctly.
- **Temperature Conversion**: Test the conversion of temperature values from Kelvin to Celsius (or Fahrenheit) based on user preference.
- **Daily Weather Summary**: Simulate weather updates for several days and verify daily summaries are calculated correctly.
- **Alerting Thresholds**: Define and configure user thresholds and verify that alerts are triggered correctly when thresholds are breached.

You can check the `tests` folder to run unit tests.



