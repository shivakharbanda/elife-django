from django.shortcuts import render, get_object_or_404
from .models import Plans
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .forms import BuyPlanForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Orders
from users.models import CustomUser

# Create your views here.

def plans(request):
    plans = Plans.objects.all()
    context = {
        'title': 'Elife - Plans',
        'plans': plans
    }
    return render(request, 'plans/plan.html', context)


class UserBuyPlan(LoginRequiredMixin, CreateView):

    model = Orders
    template_name = 'plans/plan.html'
    fields = ['pack']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
  
"""def get(self, request):
        return render(request, 'users/user.html')"""

class AutoUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    fields = ['pack']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False
