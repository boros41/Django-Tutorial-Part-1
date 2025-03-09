from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__" # all the fields in the Room model
        exclude = ['host', 'participants'] # exclude the host and participants fields

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']