from django.contrib import admin

# Register your models here.

from .models import User, GymUser

admin.site.register(User)
admin.site.register(GymUser)