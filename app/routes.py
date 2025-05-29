from flask import render_template, request, jsonify, make_response, Blueprint
from app.forms import CityForm
from app.services import get_weather_data, get_city_suggestions
from app.models import CitySearch, db
from datetime import datetime
import logging

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    last_city = request.cookies.get('last_city')

    if form.validate_on_submit():
        city_name = form.city_name.data
        weather_data = get_weather_data(city_name)

        if weather_data.get('error'):
            return render_template('index.html', form=form, error=weather_data['error'], last_city=last_city)

        city_search = CitySearch.query.filter_by(city_name=city_name).first()
        if city_search:
            city_search.search_count += 1
            city_search.last_searched = datetime.utcnow()
        else:
            city_search = CitySearch(city_name=city_name)
            db.session.add(city_search)
        db.session.commit()

        response = make_response(render_template(
            'weather.html',
            city_name=city_name,
            weather=weather_data,
            form=form
        ))
        response.set_cookie('last_city', city_name, max_age=30 * 24 * 60 * 60)
        return response

    return render_template('index.html', form=form, last_city=last_city)


@bp.route('/api/cities')
def city_suggestions():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    suggestions = get_city_suggestions(query)
    return jsonify(suggestions)


@bp.route('/api/stats')
def search_stats():
    stats = CitySearch.query.order_by(CitySearch.search_count.desc()).limit(10).all()
    return jsonify([{'city': s.city_name, 'count': s.search_count} for s in stats])
