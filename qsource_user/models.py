from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

# Create your models here.
# class SignUp(models.Model):
    # email = models.EmailField()
    # username = models.CharField(max_length=20, blank=False, null=True)
    # timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    # updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    # def _unicode_(self): #Python 3.3 is _str_
        # return self.email
        
        
class UserData(models.Model):
    user = models.OneToOneField(User, primary_key = True, related_name = "data")
    showMyQuestions = models.BooleanField(default = False)
    showLocal = models.BooleanField(default = False)
    showRecent = models.BooleanField(default = True)
    position = GeopositionField()

class QuestionsAnswered(models.Model):
    user = models.ForeignKey(UserData)
    questionID = models.IntegerField()

class QuestionsAsked(models.Model):
    user = models.ForeignKey(UserData)
    questionID = models.IntegerField()
