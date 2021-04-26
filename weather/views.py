from django.shortcuts import render
import requests


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=API_KEY'
    city = "Mumbai"
    r = requests.get(url.format(city)).json()
    city_weather_conditions = {
        'city': city,
        'temperature': r['main']['temp'],
        'feels_like': r['main']['feels_like'],
        'humidity': r['main']['humidity'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    context = {'city_weather_conditions': city_weather_conditions}
    return render(request, 'home.html', context)
