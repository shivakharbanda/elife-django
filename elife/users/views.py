from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from .forms import MakeForm
from django.http import HttpResponseRedirect as redirect
# Create your views here.

class UserRegisterView(View):
    pass


class UserCreate(View):
    template = 'users/register.html'
    #success_url = reverse_lazy('autos:all')
    success_url = reverse_lazy('login')

    def get(self, request):
        form = MakeForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = MakeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        make = form.save()
        return redirect(self.success_url)

"""def get(self, request):
        return render(request, 'users/user.html')"""

