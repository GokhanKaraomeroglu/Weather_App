from django.shortcuts import render
import requests
from decouple import config
from pprint import pprint
from .models import City
from django.contrib import messages


def index(request):
    cities = City.objects.all()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    # city = "istanbul"
    # response = requests.get(url.format(city, config('API_KEY')))
    # content = response.json()
    # pprint(content)
    # print(type(content))
    
    g_city = request.GET.get('name')
    print ('g_city: ', g_city)
    if g_city :
        response = requests.get(url.format(g_city, config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            a_city= content['name']
            print(a_city)
            if City.objects.filter(name=a_city):
                messages.warning(request, 'City already exist.')
            else:
                City.objects.create(name = a_city)
                messages.success(request, 'City successfully added.')
        else:
            messages.warning(request, 'City not found') 
            
    city_data = []
    for city in cities:
        print(city)
        response = requests.get(url.format(city, config('API_KEY')))
        content = response.json()
        pprint(content)
        tempc = round(content["main"]["temp"]- 273.15)
        # desc1 = content["weather"][0]["description"]
        # desc1.upper()
        
        data = {
            "city": city,
            "temp": tempc,
            "desc": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"]
        }
        # print(type(content))
        city_data.append(data)
    print(city_data)
    context = {
        "city_data": city_data,
    }
    return render(request, "weather_app/index.html", context)
