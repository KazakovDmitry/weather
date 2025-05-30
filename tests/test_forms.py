from app.forms import CityForm


def test_city_form():
    form = CityForm(data={'city_name': 'Москва'})
    assert form.validate() is True
    assert form.city_name.data == 'Москва'


def test_empty_city_form():
    form = CityForm(data={'city_name': ''})
    assert form.validate() is False
