import urllib
from urllib import request
from django import forms
from django.forms import ModelForm
from .models import Plans, Orders
from users.models import CustomUser


class BuyPlanForm(forms.ModelForm):

    class Meta():
        model = Orders
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        self.user = CustomUser
        super(BuyPlanForm, self).__init__(*args, *kwargs)
        self.fields['user'].initial = self.user