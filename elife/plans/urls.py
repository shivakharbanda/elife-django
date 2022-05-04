from django.urls import path
from . import views as plans_views

urlpatterns = [
    path('', plans_views.UserBuyPlan.as_view(), name = 'plans-plan'),
    path('plans-view-only/', plans_views.plans, name='plans-viewonly')
]
