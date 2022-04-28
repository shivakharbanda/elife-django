from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.

def home(request):
    context = {
        'title': 'ELIFE - HOME'
    }
    return render(request, 'home/home.html', context)

