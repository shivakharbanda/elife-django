import urllib
from urllib import request
from django import forms
from django.forms import ModelForm
from .models import Plans, Orders
from users.models import CustomUser


class BuyPlanForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    pack = forms.ModelChoiceField(Plans.objects.all(), widget=forms.RadioSelect())

    class Meta():
        model = Orders
        fields = ['pack']

    

    #def __init__(self, *args, **kwargs):
     #   super(BuyPlanForm, self).__init__(*args, **kwargs)
      #  for field in self.fields.values():
       #     if isinstance(field.widget, forms.Select):
         #       field.widget = forms.RadioSelect()


"""
class BuyPlanForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta():
        model = Orders
        fields = ['pack']

    """