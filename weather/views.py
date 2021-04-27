from django.shortcuts import render
import requests
from .models import City
from .forms import MainForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=API_KEY'

    if request.method == 'POST':
        form = MainForm(request.POST)
        form.save()

    form = MainForm()
    cities = City.objects.all()

    all_weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather_conditions = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        all_weather_data.append(city_weather_conditions)
    context = {'weather_data': all_weather_data, 'form': form}
    return render(request, 'home.html', context)
