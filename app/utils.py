from datetime import datetime


def format_temperature(temp):
    return f"{temp}°C" if temp is not None else "N/A"


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M') if timestamp else "N/A"
