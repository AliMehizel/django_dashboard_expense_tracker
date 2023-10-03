from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date

# Create your models here.
transaction_type = (
    ('EXPENSE', 'EXPENSE'),
    ('INCOME', 'INCOME')
)

class User(AbstractUser):
    avatar = models.ImageField(default='avatar/avatar.png',upload_to='avatar')
    
    
    def __str__(self):
        return self.username 
    
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desc = models.CharField( max_length=150, null=True,blank=True)
    amount = models.FloatField(blank=True,null=True)
    date_pub = models.DateField(default=date.today)
    transac_type = models.CharField(choices=transaction_type,max_length=50)
    
    def __str__(self):
        return self.desc
    
    
    