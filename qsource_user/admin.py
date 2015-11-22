from django.contrib import admin

#from .models import SignUp
from .models import UserData

# class SignUpAdmin(admin.ModelAdmin):
    # list_display = ["_unicode_", "timestamp", "updated"]
    # form = SignUpForm

# admin.site.register(SignUp, SignUpAdmin)

# UserData model for the admin.
class UserDataAdmin(admin.ModelAdmin):
    list_display = ["user", "position"]
    
admin.site.register(UserData, UserDataAdmin)
