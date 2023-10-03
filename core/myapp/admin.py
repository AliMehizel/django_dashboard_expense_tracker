from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    model = User 
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Profile',
            {
                'fields':(
                    'avatar',
                )
            }
        )
    )

admin.site.register(User, UserAdmin)
admin.site.register(Transaction)
