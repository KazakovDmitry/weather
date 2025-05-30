import requests
from functools import lru_cache


@lru_cache(maxsize=100)  # Кэшируем запросы к GeoNames
def get_city_coordinates(city_name: str, geonames_username: str) -> tuple[float, float] | None:
    """Получает широту и долготу города через GeoNames"""
    try:
        url = f"http://api.geonames.org/searchJSON?name={city_name}&maxRows=1&username={geonames_username}"
        response = requests.get(url)
        data = response.json()
        if data.get('geonames'):
            return data['geonames'][0]['lat'], data['geonames'][0]['lng']
        return None
    except requests.exceptions.RequestException as e:
        print(f"GeoNames API error: {e}")
        return None


@lru_cache(maxsize=100)  # Кэшируем запросы к Open-Meteo
def get_weather_by_coords(latitude: float, longitude: float) -> dict:
    """Получает прогноз погоды по координатам через Open-Meteo"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Open-Meteo API error: {e}")
        return {'error': 'Weather data fetch failed'}
