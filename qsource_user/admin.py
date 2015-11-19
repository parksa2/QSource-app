from django.contrib import admin

#Register your models here.

#from .models import SignUp
from .models import UserData

# class SignUpAdmin(admin.ModelAdmin):
    # list_display = ["_unicode_", "timestamp", "updated"]
    # form = SignUpForm

# admin.site.register(SignUp, SignUpAdmin)

class UserDataAdmin(admin.ModelAdmin):
    list_display = ["user", "position"]
    
admin.site.register(UserData, UserDataAdmin)