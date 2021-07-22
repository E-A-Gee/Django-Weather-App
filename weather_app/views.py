from django.shortcuts import render
import requests
# Create your views here.

def index(request):
    if request.method=="POST":
        search_city = request.POST.get('search-city')

        return render(request, 'weather_app/weather.html',{})

    else:
        # Get user IP address
        user_ip = request.META.get("REMOTE_ADDR")
        
        # Get user longitude and latitude
        ip_response = requests.get(f'http://ip-api.com/json/{user_ip}').json()
        print(ip_response)
        user_lat = ip_response['lat']
        user_lon = ip_response['lon']
        city = ip_response['city']
        
        #OpenWeatherAPI
        open_weather_url= f'api.openweathermap.org/data/2.5/weather?lat={user_lat}&lon={user_lon}&appid=65d6a2854eae556a61d30eaa38bea1a6'
        weather_response = requests.get(open_weather_url).json()

        city_weather = {
            'city': city,
            'temperature': weather_response['main']['temp'],
            'description':weather_response[0]['description'],
            'icon': weather_response['weather'][0]['description']
        }

        context = {'city_weather':city_weather}

        return render(request, 'weather_app/weather.html', context)
        # remember to enter in context