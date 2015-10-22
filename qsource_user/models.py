from django.db import models

# Create your models here.
class SignUp(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=20, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def _unicode_(self): #Python 3.3 is _str_
        return self.email