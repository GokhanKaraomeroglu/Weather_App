from django.shortcuts import render
import requests
from decouple import config

def index(request):
    url= 'https//api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    city = 'istanbul'
    response = requests.get(url.format(city, config('API_KEY')))
    return render(request, "weather_app/index.html")