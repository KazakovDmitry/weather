from flask import render_template, request, current_app, Blueprint, make_response
from datetime import datetime
from app.forms import CityForm
from app.services import get_city_coordinates, get_weather_by_coords
from app.models import CitySearch, db

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    last_city = request.cookies.get('last_city')  # Получаем последний город из cookies

    if form.validate_on_submit():
        city_name = form.city_name.data
        # Получаем координаты
        coords = get_city_coordinates(city_name, current_app.config['GEONAMES_USERNAME'])
        if not coords:
            return render_template('index.html', form=form, error="Город не найден", last_city=last_city)

        # Получаем погоду
        weather_data = get_weather_by_coords(*coords)
        if weather_data.get('error'):
            return render_template('index.html', form=form, error=weather_data['error'], last_city=last_city)

        # Сохраняем в историю
        city_search = CitySearch.query.filter_by(city_name=city_name).first()
        if city_search:
            city_search.search_count += 1
            city_search.last_searched = datetime.utcnow()
        else:
            city_search = CitySearch(city_name=city_name)
            db.session.add(city_search)
        db.session.commit()

        # Создаем response и устанавливаем cookie
        response = make_response(render_template(
            'weather.html',
            city_name=city_name,
            weather=weather_data
        ))
        response.set_cookie(
            'last_city',
            value=city_name,
            max_age=30 * 24 * 60 * 60,  # 30 дней
            secure=True,  # Только для HTTPS
            httponly=True,  # Защита от XSS
            samesite='Lax'  # Безопасная политика
        )
        return response

    return render_template('index.html', form=form, last_city=last_city)