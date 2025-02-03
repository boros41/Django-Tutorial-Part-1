from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#  list of rooms containing a dictionary each containing an ID and name
rooms = [
    {"id":1, "name":"Leats learn python!"},
    {"id":2, "name":"Design with me!"},
    {"id":3, "name":"Frontend developers"},
]

# home page
def home(request):
    context = {"rooms": rooms}
    return render(request, 'base/home.html', context)

# room page for different conversations
def room(request, pk):
    room = None # no room when we first go to link

    for i in rooms:
        if i["id"] == int(pk): # if the room ID matches the ID (pk) of the clicked link, that is our room
            room = i

    context = {"room": room}
    return render(request, "base/room.html", context) # return a specific page for a room