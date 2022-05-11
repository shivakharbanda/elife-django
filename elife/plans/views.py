from django.shortcuts import render, get_object_or_404
from .models import Plans
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .forms import BuyPlanForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Orders
from users.models import CustomUser
from django.http import HttpResponseRedirect as redirect

# Create your views here.

def plans(request):
    plans = Plans.objects.all()
    context = {
        'title': 'Elife - Plans',
        'plans': plans
    }
    return render(request, 'plans/plans_view_only.html', context)

class UserBuyPlan(LoginRequiredMixin, View):
    template = 'plans/plan.html'
    success_url = reverse_lazy('payment- summary')
    login_url = '/login/'

    def get(self, request):
        plans = Plans.objects.all()
        form = BuyPlanForm()
        
        ctx = {
            'form': form,
            'plans': plans,
        }
        return render(request, self.template, ctx)

    def post(self, request):
        form = BuyPlanForm(request.POST)
        form.instance.user = self.request.user
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        make = form.save()
        return redirect(self.success_url)

"""
class UserBuyPlan(LoginRequiredMixin, CreateView):
    template_name = 'plans/plan.html'
    form_class = BuyPlanForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
  
"""

"""class AutoUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    fields = ['pack']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False"""


class  AutoUpdate(LoginRequiredMixin, View):
    model = Orders
    template = 'plans/orders_form.html'
    success_url = reverse_lazy('home-home')

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        plans = Plans.objects.all()
        form = BuyPlanForm()
        
        ctx = {
            'form': form,
            'plans': plans,
        }
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = BuyPlanForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

