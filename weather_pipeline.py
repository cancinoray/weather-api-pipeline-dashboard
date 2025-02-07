import os
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import schedule
import time
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOG_DIR = './logs'  # Ensure logs are saved to the 'logs' folder
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{LOG_DIR}/weather_pipeline.log'),
        logging.StreamHandler()
    ]
)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
DB_CONNECTION = os.getenv('DATABASE_URL')
CITIES = ['London', 'New York', 'Tokyo']  # Add your cities here
ENGINE = create_engine(DB_CONNECTION)
OUTPUT_DIR = './plots'  # Save plots to the 'plots' folder


def fetch_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API for a given city."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        logging.info(f"Fetched data: {data}")

        return {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description'],
            'timestamp': datetime.now()
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {str(e)}")
        return None


def store_weather_data(data, engine):
    """Store weather data in PostgreSQL database."""
    if not data:
        return

    try:
        df = pd.DataFrame([data])
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        logging.info(f"Successfully stored weather data for {data['city']}")
    except Exception as e:
        logging.error(f"Error storing data in database: {str(e)}")

# def analyze_weather_data(city, engine):
#     """Analyze weather data for the past 7 days."""
#     try:
#         query = f"""
#             SELECT *
#             FROM weather_data
#             WHERE city = '{city}'
#             AND timestamp >= NOW() - INTERVAL '7 days'
#             ORDER BY timestamp;
#         """

#         df = pd.read_sql(query, engine)

#         if df.empty:
#             logging.warning(f"No data found for {city} in the past 7 days")
#             return

#         avg_temp = df['temperature'].mean()
#         avg_humidity = df['humidity'].mean()

#         plt.figure(figsize=(10, 6))
#         plt.plot(df['timestamp'], df['temperature'], marker='o')
#         plt.title(f'Temperature Trend - {city}')
#         plt.xlabel('Date')
#         plt.ylabel('Temperature (°C)')
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.savefig(f'temperature_trend_{city}.png')
#         plt.close()

#         logging.info(f"""
#             Analysis for {city} (past 7 days):
#             Average Temperature: {avg_temp:.1f}°C
#             Average Humidity: {avg_humidity:.1f}%
#         """)

#     except Exception as e:
#         logging.error(f"Error analyzing data: {str(e)}")


def analyze_weather_data(city, engine):
    try:
        query = f"""
            SELECT *
            FROM weather_data
            WHERE city = '{city}'
            AND timestamp >= NOW() - INTERVAL '7 days'
            ORDER BY timestamp;
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            logging.warning(f"No data found for {city} in the past 7 days")
            return

        avg_temp = df['temperature'].mean()
        avg_humidity = df['humidity'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['temperature'], marker='o')
        plt.title(f'Temperature Trend - {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Ensure the 'plots' directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Save plot in the 'plots' directory
        file_path = os.path.join(OUTPUT_DIR, f'temperature_trend_{city}.png')
        plt.savefig(file_path)
        plt.close()

        logging.info(f"Graph saved to {file_path}")
        logging.info(f"""
            Analysis for {city} (past 7 days):
            Average Temperature: {avg_temp:.1f}°C
            Average Humidity: {avg_humidity:.1f}%
        """)

    except Exception as e:
        logging.error(f"Error analyzing data: {str(e)}")


def run_pipeline():
    """Run the complete pipeline for all cities."""
    for city in CITIES:
        data = fetch_weather_data(city, API_KEY)
        store_weather_data(data, ENGINE)
        analyze_weather_data(city, ENGINE)


def main():
    schedule.every().day.at("08:00").do(run_pipeline)
    run_pipeline()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
