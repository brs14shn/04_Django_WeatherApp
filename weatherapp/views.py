from django.shortcuts import render,redirect,get_object_or_404
from decouple import config
import requests # İstek(get) isteği
from pprint import pprint # gelen veriyi daha okunaklı hale getirdik
from django.contrib import messages

from .models import City



  

def index(request):
    API_KEY = config('API_KEY')
    user_city=request.POST.get("name")
    city = "Bursa"
    if user_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API_KEY}&units=metric"
        response= requests.get(url)
        print(response.ok) #! True

        if response.ok:
           content = response.json() #? dictionary yapısına çevirmiş olduk
           r_city=content["name"]
           if City.objects.filter(name=r_city):
                messages.warning(request, 'City already exists!')
           else:
                City.objects.create(name=r_city)
                messages.success(request, 'City created!')

        else:
             messages.warning(request, 'There is no city!')
    city_data=[]
    cities=City.objects.all()
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data={
                # "city":content["name"],
                "city":city,
                 "temp":content['main']['temp'],
                "icon":content['weather'][0]['icon'],
                "desc":content['weather'][0]['description']

        }
        city_data.append(data)
        pprint(city_data)

    context={
       "city_data":city_data
    }
    return render(request, 'weatherapp/index.html',context)

def delete_city(request, id):
        city = get_object_or_404(City, id=id)
        city.delete()
        messages.success(request, 'City deleted!')
        return redirect('home')

    