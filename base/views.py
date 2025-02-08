from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.


#  list of rooms containing a dictionary each containing an ID and name
# rooms = [
#     {"id":1, "name":"Leats learn python!"},
#     {"id":2, "name":"Design with me!"},
#     {"id":3, "name":"Frontend developers"},
# ]


# home page
def home(request):
    rooms = Room.objects.all() # get all the rooms in the database (entries), currently overriding rooms list
    context = {"rooms": rooms}
    return render(request, 'base/home.html', context)

# room page for different conversations
def room(request, pk):
    room = Room.objects.get(id=pk) # gets room object/entry where the id (primary key) is equal to the URL clicked i.e, room/1

    # for i in rooms:
    #     if i["id"] == int(pk): # if the room ID matches the ID (pk) of the clicked link, that is our room
    #         room = i

    context = {"room": room}
    return render(request, "base/room.html", context) # return a specific page for a room

def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST) # get the user's input from the form contained in the POST request

        if form.is_valid():
            form.save() # save the user's input of the model instance to the database
            return redirect("home") # redirect to the home page specified by the url's name attribute
    

    context = {"form": form}
    return render(request, "base/room_form.html", context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # gets room object/entry where the id (primary key) is equal to the URL clicked i.e, room/1
    form = RoomForm(instance=room) # prefill the form with the selected room model's data since we want to know what we are editing
    
    if request.method == "POST":
        # get the user's input of the selected room from the form contained in the POST request
        form = RoomForm(request.POST, instance=room) # data in POST request will replace whatever is in the room instance
        if form.is_valid():
            form.save()
            return redirect("home") # redirect to the home page specified by the url's name attribute 

    context = {"form": form}
    return render(request, "base/room_form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete() # remove room entry from Room table from the database
        return redirect("home")

    return render(request, "base/delete.html", {"obj":room})