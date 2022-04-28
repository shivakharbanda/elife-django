from django.contrib import admin

# Register your models here.

from .models import Plans, Orders



admin.site.register(Plans)
admin.site.register(Orders)