from requests import request
import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    api_wheather_token = '19b818fecab72ccd0d8badaf71d418b5'

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_wheather_token

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    try:
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': int(res["main"]['temp']),
                'icon': res['weather'][0]['icon']
            }
            all_cities.append(city_info)
    except KeyError:
        pass

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)
