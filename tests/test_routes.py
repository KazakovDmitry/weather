from unittest.mock import patch


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Прогноз погоды' in response.data


def test_city_suggestions_route(client):
    response = client.get('/api/cities?q=Mos')
    assert response.status_code == 200
    assert response.is_json


def test_city_suggestions(client):
    with patch('app.services.get_city_suggestions') as mock_suggest:
        mock_suggest.return_value = ['Moscow, Russia']
        response = client.get('/api/cities?q=Mos')
        assert response.json == ['Moscow, Russia']


def test_index_handles_geonames_error(client, mock_geonames):
    """Тест обработки ошибки GeoNames в роуте /"""
    mock_geonames.return_value.json.return_value = {"geonames": []}
    response = client.post("/", data={"city_name": "UnknownCity"})
    assert b"Город не найден" in response.data


def test_api_cities_handles_error(client, mock_geonames):
    """Тест обработки ошибки в /api/cities"""
    mock_geonames.side_effect = Exception("API error")
    response = client.get("/api/cities?q=Mos")
    assert response.json == []


def test_index_post_invalid_form(client):
    response = client.post('/', data={'city_name': ''})
    assert b'This field is required' in response.data

