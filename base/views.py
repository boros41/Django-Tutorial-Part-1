from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home page
def home(request):
    return HttpResponse("Home page")

# room page for different conversations
def room(request):
    return HttpResponse('ROOM') # return a specific page for a room