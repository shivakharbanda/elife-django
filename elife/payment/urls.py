from django.urls import path
from . import views as payment_views

urlpatterns = [
    path('plans-view-only/', payment_views.payment, name='payment- summary'),
]
