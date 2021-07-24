from django.shortcuts import render
import requests
from ipware import get_client_ip
# Create your views here.

def index(request):
    #Get user ip address
    user_ip, is_routable = get_client_ip(request)

    # Get user longitude and latitude
    ip_response = requests.get(f'http://ip-api.com/json/{user_ip}').json()
    print(ip_response)
    user_lat = ip_response['lat']
    user_lon = ip_response['lon']
    city = ip_response['city']

    #OpenWeatherAPI - Weather info from lat and lon
    open_weather_url= f'api.openweathermap.org/data/2.5/weather?lat={user_lat}&lon={user_lon}&appid=65d6a2854eae556a61d30eaa38bea1a6'
    weather_response = requests.get(open_weather_url).json()

    city_weather = {
        'user_ip':is_routable,
        'city': city,
        'temperature': weather_response['main']['temp'],
        'description':weather_response[0]['description'],
        'icon': weather_response['weather'][0]['description']
    }
        
    return render(request, 'weather_app/weather.html', city_weather)


    if request.method=="POST":
        search_city = request.POST.get('search-city')

        return render(request, 'weather_app/weather.html',{})

    # else:

        

        



