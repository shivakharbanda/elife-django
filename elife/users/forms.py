from django.forms import ModelForm
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class MakeForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','first_name', 'last_name', 'Address')