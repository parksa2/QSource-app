import datetime
from django.utils import timezone
from django.db import models


#Question model: represents one poll with question, answers, votes.
#Many-to-many relationship with UserData model: see qsource-user/models.py
class Question(models.Model):
    #basic poll info
    question_text = models.CharField(max_length = 300)    
    ans1_text = models.CharField(max_length = 80, default= "Yes")
    ans1_votes = models.IntegerField(default = 0)
    ans2_text = models.CharField(max_length = 80, default = "No")
    ans2_votes = models.IntegerField(default = 0)
    
    #storing publication date allows sorting by most recent
    pub_date = models.DateTimeField('date published')
    #storing total votes allows sorting by popularity
    votes = models.IntegerField(default = 0)
    
    #generate a string to represent the object
    def __unicode__(self):
        return self.question_text
    
    #returns true for questions published in the last day
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    #specifications for appearance of was_published_recently attribute on admin site
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    #Question manages its own data by tallying new votes in member function
    def vote(self, ans_num):
        if(int(ans_num) == 0): 
            self.ans1_votes += 1    
        elif(int(ans_num) == 1): 
            self.ans2_votes += 1
        self.votes = self.ans1_votes + self.ans2_votes
