import requests
from functools import lru_cache
from flask import current_app
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@lru_cache(maxsize=100, ttl=600)
def get_weather_data(city_name):
    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={current_app.config['OPENWEATHER_API_KEY']}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()

        if not geo_response.json():
            return {'error': 'Город не найден'}

        lat = geo_response.json()[0]['lat']
        lon = geo_response.json()[0]['lon']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()

        return weather_response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return {'error': 'Ошибка при получении данных о погоде'}


def get_city_suggestions(query):
    try:
        url = f"http://api.geonames.org/searchJSON?name_startsWith={query}&maxRows=10&username={current_app.config['GEONAMES_USERNAME']}&cities=cities1000"
        response = requests.get(url)
        response.raise_for_status()
        return [city['name'] + ', ' + city.get('countryName', '') for city in response.json().get('geonames', [])]
    except requests.exceptions.RequestException as e:
        logger.error(f"GeoNames API error: {e}")
        return []
    