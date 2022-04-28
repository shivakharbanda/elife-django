import datetime
from datetime import datetime as dt
from datetime import timedelta
from django.db import models
from users.models import CustomUser
from django.urls import reverse


# Create your models here.

class Plans(models.Model):
    plan_name = models.CharField(max_length=50)
    speed = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.plan_name

def get_deadline():
    return dt.today() + timedelta(days=30)


class Orders(models.Model):
    user = models.ForeignKey(CustomUser, primary_key=True, on_delete = models.CASCADE)
    pack = models.ForeignKey(Plans, on_delete = models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=get_deadline())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        name = str(self.user.username)
        return name

    def get_absolute_url(self):
        return reverse('home-home')