# Generated by Django 4.0.4 on 2022-04-28 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_alter_orders_end_date_alter_orders_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 28, 17, 33, 46, 660154)),
        ),
    ]
