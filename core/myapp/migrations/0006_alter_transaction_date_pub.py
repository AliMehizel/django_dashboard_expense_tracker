# Generated by Django 4.2.5 on 2023-09-29 14:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_transaction_date_on_transaction_date_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_pub',
            field=models.DateField(default=datetime.date.today),
        ),
    ]