import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///weather.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEONAMES_USERNAME = os.environ.get('GEONAMES_USERNAME')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
