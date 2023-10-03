from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm

""" transaction_type = (
    ('EXPENSE', 'EXPENSE'),
    ('INCOME', 'INCOME')
) """
class SigninForm(forms.Form):
    username = forms.CharField(label='Username',max_length=150, required=True)
    password = forms.CharField(max_length=32, label='Password',widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
class SignupForm(UserCreationForm):
    #email = forms.EmailField(label='Email', required=True)
    class Meta:
        model = User
        fields= ['username', 'email', 'password1', 'password2']
        
        
class CustomPasswordChangeForm(forms.Form):
    current_password = forms.CharField(max_length=32, label='Current password',widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=32, label='New password',widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(max_length=32, label='Confirm new Password',widget=forms.PasswordInput)

class TransactionForm(forms.ModelForm):
    desc = forms.CharField(label="Description", max_length=200, required=False)
    amount = forms.FloatField(label='Amount', required=False)
    transac_type = forms.ChoiceField(label='Category', choices=transaction_type, required=False)
    class Meta:
        model = Transaction
        fields= ['desc', 'amount','transac_type']



class PostSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='', required=False)