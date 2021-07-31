from django.shortcuts import render
import requests
from ipware import get_client_ip
# Create your views here.

def index(request):
    #if using the searchbar
    if request.method=="POST":
        search_city = request.POST.get('search-city')
        if search_city.isnumeric():
            open_weather_url= f'http://api.openweathermap.org/data/2.5/weather?zip={search_city},US&units=imperial&appid=65d6a2854eae556a61d30eaa38bea1a6'
        else:
            open_weather_url= f'http://api.openweathermap.org/data/2.5/weather?q={search_city}&units=imperial&appid=65d6a2854eae556a61d30eaa38bea1a6'
        weather_response = requests.get(open_weather_url).json()
        city = weather_response['name']

    #if getting ip address
    else:
        #Get user ip address
        user_ip, is_routable = get_client_ip(request)

        # Get user longitude and latitude
        ip_response = requests.get(f'http://ip-api.com/json/{user_ip}').json()
        
        user_lat = ip_response['lat']
        user_lon = ip_response['lon']
        city = ip_response['city']

        #OpenWeatherAPI - Weather info from lat and lon
        open_weather_url= f'http://api.openweathermap.org/data/2.5/weather?lat={user_lat}&lon={user_lon}&units=imperial&appid=65d6a2854eae556a61d30eaa38bea1a6'
        weather_response = requests.get(open_weather_url).json()
    if weather_response['cod'] == '404':
        city_weather = {'error':'City not found.'}
    else:
        city_weather = {
            'city': city,
            'temperature': weather_response['main']['temp'],
            'description':weather_response['weather'][0]['description'],
            'icon': weather_response['weather'][0]['icon']
        }
        
    return render(request, 'weather_app/weather.html', city_weather)
