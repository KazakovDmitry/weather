# Приложение прогноза погоды

Приложение для просмотра прогноза погоды по названию города.

## Функции
- Поиск погоды по городу
- Автодополнение при вводе города
- История поиска (cookies)
- API статистики популярных городов
- Docker поддержка
- Тесты (pytest)

## Запуск

### Локально
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите: `flask run`
3. Откройте http://localhost:5000

### Docker
1. Создайте .env файл с API ключами:
GEONAMES_USERNAME=dimakameya
FLASK_APP=app
DATABASE_URL=sqlite:///weather.db

2. Запустите: `docker-compose up`
3. Откройте http://localhost:5000

## API
- `/api/cities?q=<query>` - поиск городов
- `/api/stats` - статистика поиска