from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages

# Create your views here.

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=81b7eb80746f1ee1ca275e36323291f5&units=metric'

    if request.method=="POST":
        form=CityForm(request.POST)        
        if form.is_valid():
            NCity=form.cleaned_data['name']            
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                response=requests.get(url.format(NCity)).json()                
                if response['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully...!!!")
                else: 
                    messages.error(request,"City Does Not Exists...!!!")
            else:
                messages.error(request,"City Already Exists...!!!")      

    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:        
        response=requests.get(url.format(city)).json()   
        city_weather={
            'city':city,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
            'country' : response['sys']['country'],
            'icon' : response['weather'][0]['icon'],
        }
        data.append(city_weather)  
    context={'data' : data,'form':form}
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('Home')