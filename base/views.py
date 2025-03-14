from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required # decorator to ensure that the user is logged in
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm
from .forms import RoomForm, UserForm, MyUserCreationForm


# Create your views here.


#  list of rooms containing a dictionary each containing an ID and name
# rooms = [
#     {"id":1, "name":"Leats learn python!"},
#     {"id":2, "name":"Design with me!"},
#     {"id":3, "name":"Frontend developers"},
# ]


def loginPage(request):
    page = "login"

    if request.user.is_authenticated: # if the user is already logged in, redirect to the home page
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email) # will throw an exception if the user does not exist
        except:
            messages.error(request, "User does not exist")

        # return a User object if credentials are valid, None otherwise
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user) # adds the user to the sessions database table and stores it as a cookie in the user's browser
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")

    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request) # deletes the token therefore deleting that user
    return redirect("home")

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST) # pass the user's credentials from the register form contained in the POST request
        if form.is_valid():
            user = form.save(commit=False) # save the user's credentials to the database but do not commit yet
            user.username = user.username.lower() # convert the username to lowercase
            user.save() # commit the user's credentials to the database
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'base/login_register.html', {'form': form})

# home page
def home(request):
    if request.GET.get("q") != None:
        q = request.GET.get("q") # get the query parameter from the URL such as "?q=Django"
    else:
        q = ""

    # get the room objects/entries where the topic name is equal to the query parameter
    # this goes into the topic field of model Room and goes to the parent using (__) to get the name to see if it is equal to q
    # the __icontains is a case-insensitive search meaning if the query is empty, then technically all topic names match that
    # if the query is not empty but only contains the start of a topic name such as "Un" for "Unity" then it will
    # still match the topic name "Unity" because it contains "Un", hence the name "contains"
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q)
        | Q(host__username__icontains=q)) # room name

    room_count = rooms.count() # get the number of rooms 

    topics = Topic.objects.all()[0:5] # get all the topics in the database (entries), ideally would filter if a lot of topics

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, 'base/home.html', context)

# room page for different conversations
def room(request, pk):
    room = Room.objects.get(id=pk) # gets room object/entry where the id (primary key) is equal to the URL clicked i.e, room/1

    # for i in rooms:
    #     if i["id"] == int(pk): # if the room ID matches the ID (pk) of the clicked link, that is our room
    #         room = i

    room_messages = room.message_set.all() # get all the messages in the room
    participants = room.participants.all() # get all the participants in the room

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user) # add the user to the room's participants
        return redirect("room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context) # return a specific page for a room

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name) # get the topic object if it exists, otherwise create it
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description")
        )

        return redirect("home") # redirect to the home page specified by the url's name attribute
    

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url="/login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # gets room object/entry where the id (primary key) is equal to the URL clicked i.e, room/1
    form = RoomForm(instance=room) # prefill the form with the selected room model's data since we want to know what we are editing
    topics = Topic.objects.all()

    if request.user != room.host: # if the user is not the host of the room, they cannot edit the room
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name) # get the topic object if it exists, otherwise create it
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home") # redirect to the home page specified by the url's name attribute 

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)

@login_required(login_url="/login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host: # if the user is not the host of the room, they cannot delete the room
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        room.delete() # remove room entry from Room table from the database
        return redirect("home")

    return render(request, "base/delete.html", {"obj":room})

@login_required(login_url="/login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user: # if the user is not the host of the room, they cannot delete the room
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        message.delete() # remove room entry from Room table from the database
        return redirect("home")

    return render(request, "base/delete.html", {"obj":message})

@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    if request.GET.get("q") != None:
        q = request.GET.get("q") # get the query parameter from the URL such as "?q=Django"
    else:
        q = ""

    topics = Topic.objects.filter(name__icontains=q) 
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})