import requests

with open('bot_weather_api.txt', 'r') as f:
    weather_api = f.read()


def fetch_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  
    else:
        return None

def format_weather_message(weather_data):
    city = weather_data['name']
    try:
        weather_description = get_weather_description(weather_data['weather'][0]['description'])
    except:
        weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp'] - 273.15
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    icon = get_weather_icon(weather_data['weather'][0]['icon'])
    message = f"Ob havo malumoti {city}: {icon} {weather_description}\nHarorat: {temperature:.2f}°C\nNamlik: {humidity}%\nShamol Tezligi: {wind_speed} m/s"
    return message

def get_weather_icon(icon_code):
    icons = {
        "01d": "☀️",
        "01n": "🌙",
        "02d": "⛅️",
        "02n": "🌙⛅️",
        "03d": "☁️",
        "03n": "☁️",
        "04d": "☁️",
        "04n": "☁️",
        "09d": "🌧",
        "09n": "🌧",
        "10d": "🌦",
        "10n": "🌧",
        "11d": "⛈",
        "11n": "⛈",
        "13d": "❄️",
        "13n": "❄️",
        "50d": "🌫",
        "50n": "🌫",
    }
    return icons.get(icon_code, "")

def get_weather_description(description):
    descriptions = {
        'overcast clouds': 'Bulutli',
        'broken clouds': 'Yarim Bulutli',
        'mist': 'Tumanli',
        'scattered clouds': 'Qisman Bulutli',
        'few clouds': 'Bulut Kam'
    }
    return descriptions[description]