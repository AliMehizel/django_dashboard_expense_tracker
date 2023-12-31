# Generated by Django 4.2.5 on 2023-09-27 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=150, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('date_on', models.DateField(auto_now=True)),
                ('transac_type', models.CharField(choices=[('EXPENSE', 'EXPENSE'), ('INCOME', 'INCOME')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
