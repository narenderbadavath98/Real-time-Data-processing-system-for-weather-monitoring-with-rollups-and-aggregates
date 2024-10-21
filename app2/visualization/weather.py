import matplotlib.pyplot as plt
import seaborn as sns

def plot_daily_weather_summary(data):
    daily_summary = get_daily_weather_summary(data)

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=daily_summary, x='date', y='temperature', label='Avg Temperature', marker='o')
    plt.title('Daily Weather Summary')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/daily_weather_summary.png')
    plt.close()

def plot_historical_trends(data):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=data, x='date', y='temperature', label='Temperature Trend', marker='o')
    plt.title('Historical Weather Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/historical_trends.png')
    plt.close()

def plot_triggered_alerts(data):
    triggered_alerts = get_triggered_alerts(data)

    plt.figure(figsize=(10, 5))
    sns.countplot(data=triggered_alerts, x='alert_type')  # Replace with your alert field
    plt.title('Triggered Alerts Count')
    plt.xlabel('Alert Type')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/triggered_alerts.png')
    plt.close()
