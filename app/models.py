from app import db
from datetime import datetime


class CitySearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    search_count = db.Column(db.Integer, default=1)
    last_searched = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CitySearch {self.city_name}>'
