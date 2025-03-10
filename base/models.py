from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True) 
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200) # a topic should not be more than 200 characters

    def __str__(self):
        return self.name

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # column representing the actual user that will be connected to the room
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # every room can have only one topic (many-to-one)
    name = models.CharField(max_length=200) # a text field of the room name

    # Null is set to false by default meaning an instance of this class (a row of the database) cannot be created
    # unless the attributes are defined with a value. Setting it to true means the model can be created without
    # setting that attribute with a value.
    # Setting blank to True means that when use the save method, when we submit a form, means that this
    # attribute can be left blank. I.e., a user can create a room without initially setting a description if they
    # want to add a description later
    description = models.TextField(null=True, blank=True) # a bigger text field than CharField of room description

    participants = models.ManyToManyField(User, related_name='participants', blank=True) # all the users currently active in a room
    
    # takes a snapshot anytime this model instance was updated. 
    # Anytime we run a save method to update this table it's gonna take a timestamp
    # everytime the save method is called, take a timestamp of the date & time
    # auto_now takes a snapshot everytime we save this model/instance
    updated = models.DateTimeField(auto_now=True) # when the room was updated

    # auto_now_add only takes a timestamp/snapshot when we first create this model/instance
    created = models.DateTimeField(auto_now_add=True) # when the room was created

    class Meta:
        # order the rooms by the date they were updated and created (columns). Minus sign means reverse chronological order
        # i.e., the most recent room will be at the top
        ordering = ['-updated', '-created'] 

    def __str__(self):
        return self.name

class Message(models.Model):
    # a user can have many messages
    # a message can have one user
    user = models.ForeignKey(User, on_delete=models.CASCADE) # when a user gets deleted, delete all Messages

    # links each message to a room. this room column will be a foreign key to Room table's id primary key
    # one room can have many messages (one-to-many)
    # each message can have one room (many-to-one), specified below
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # when a Room gets deleted, delete all Messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # when the room was updated
    created = models.DateTimeField(auto_now_add=True) # when the room was created

    class Meta:
        # order the rooms by the date they were updated and created (columns). Minus sign means reverse chronological order
        # i.e., the most recent room will be at the top
        ordering = ['-updated', '-created'] 

    def __str__(self):
        return self.body[0:50]