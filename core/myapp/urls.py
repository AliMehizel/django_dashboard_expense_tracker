from django.urls import path
from .views import *
""" 
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

"""
    
urlpatterns = [
    path('', index, name='login_page'),
    path('home/', home, name='home_page'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('data_flow/', get_transaction_amount, name='transaction_amount_list'),
    path('new_transaction/', add_new_transaction, name='new_transaction'),
    path('edit_transaction/<str:desc>/', edit_transaction, name='edit_transaction'),
    path('delete_transaction/<str:desc>/', delete_transaction, name='delete_transaction'),
    path('transaction_csv/',transactions_csv, name='transaction_csv'),
    path('transaction_pdf/',transactions_pdf, name='transaction_pdf'),
    path('change_password/', custom_password_change, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
    
    #path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),name='password-reset'),
    #path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    #path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    #path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
]
