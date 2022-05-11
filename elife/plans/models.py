import datetime
from datetime import datetime as dt
from datetime import timedelta, timezone
from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils import timezone


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
    payment_status_choices = (
        (1, "SUCCESS"), 
        (2, "FAILURE"),
        (3, "PENDING")
    )
    user = models.ForeignKey(CustomUser, primary_key=True, on_delete = models.CASCADE)
    pack = models.ForeignKey(Plans, on_delete = models.CASCADE)
    total_amount = models.FloatField(null=True)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    start_date = models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(default=get_deadline())
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    delivered = models.BooleanField(default=False)

    #related to razorpay

    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.user:
            self.order_id = self.datetime_of_payment.strftime("ELIFE%Y%m%dODR") + str(self.user)
        return super().save(*args, **kwargs)
    

    def __str__(self):
        name = str(self.user.username)
        return name

    def get_absolute_url(self):
        return reverse('home-home')