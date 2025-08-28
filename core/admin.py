from django.contrib import admin

# Register your models here.
from .models import User, LoginActivity
admin.site.register(User)
admin.site.register(LoginActivity)