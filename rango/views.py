import rango
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>") #ch3 ex. added a hyperlink to the about page

#ch3 Exercises 
def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>") #ch3 ex. added a hyperlink to the index page