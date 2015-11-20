from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from polls.models import Question
from django.utils import timezone

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
    
    def answer(self, question, choice_num):
        newAns = QuestionsAnswered.objects.create(user = self, questionID = question.pk)
        newAns.save()
        question.vote(choice_num)
        question.save()
        
    def ask(self, new_question_text, option1, option2):
        newQuestion = Question.objects.create(question_text = new_question_text,
                                              ans1_text = option1,
                                              ans2_text = option2,
                                              pub_date = timezone.now())
        newQuestion.save()
        asked = QuestionsAsked.objects.create(user = self,
                                                questionID = newQuestion.pk)
        asked.save() 

class QuestionsAnswered(models.Model):
    user = models.ForeignKey(UserData)
    questionID = models.IntegerField()

class QuestionsAsked(models.Model):
    user = models.ForeignKey(UserData)
    questionID = models.IntegerField()
