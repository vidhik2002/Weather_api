from django.shortcuts import render
import requests
from .models import City
from .forms import MainForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=b0f11ba775d36e6d23cc493a249875af'
    error = ""
    msg = ""
    msg_class = ""

    if request.method == 'POST':
        form = MainForm(request.POST)

        if form.is_valid():
            fresh_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=fresh_city).count()
            if city_count == 0:
                req = requests.get(url.format(fresh_city)).json()
                if req['cod'] == 200:
                    form.save()
                else:
                    error = "City doesnot exist "
            else:
                error = "City already there"

        if error:
            msg = error
            msg_class = 'is-danger'
        else:
            msg = "City added successfully"
            msg_class = 'is-success'
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
    context = {'weather_data': all_weather_data,
               'form': form,
               'msg': msg,
               'msg_class': msg_class
            }
    return render(request, 'home.html', context)
