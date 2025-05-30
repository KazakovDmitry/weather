import pytest
from unittest.mock import patch
from app.services import get_city_coordinates, get_weather_by_coords, get_city_suggestions


# Тест для GeoNames
def test_get_city_coordinates():
    with patch('requests.get') as mock_get:
        mock_data = {
            'geonames': [{
                'lat': '55.75',
                'lng': '37.61',
                'name': 'Moscow',
                'countryName': 'Russia'
            }]
        }
        mock_get.return_value.json.return_value = mock_data
        coords = get_city_coordinates('Moscow', 'test_username')
        assert coords == (55.75, 37.61)


# Тест для Open-Meteo
def test_get_weather_by_coords():
    with patch('requests.get') as mock_get:
        mock_data = {
            'current_weather': {
                'temperature': 20.5,
                'windspeed': 10.3
            },
            'hourly': {
                'time': ['2023-09-01T00:00'],
                'temperature_2m': [20.5]
            }
        }
        mock_get.return_value.json.return_value = mock_data
        weather = get_weather_by_coords(55.75, 37.61)
        assert 'current_weather' in weather


def test_get_city_coordinates_api_error():
    """Тест ошибки при запросе к GeoNames"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("API недоступен")
        result = get_city_coordinates("Moscow", "test_user")
        assert result is None


def test_get_city_coordinates_empty_response():
    """Тест пустого ответа от GeoNames"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"geonames": []}
        result = get_city_coordinates("UnknownCity", "test_user")
        assert result is None


def test_get_weather_by_coords_network_error():
    """Тест ошибки сети при запросе к Open-Meteo"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")
        result = get_weather_by_coords(0, 0)
        assert "error" in result


def test_get_city_suggestions_failure():
    """Тест ошибки в автодополнении городов"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("GeoNames error")
        result = get_city_suggestions("Mos")
        assert result == []
