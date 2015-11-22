import datetime
from django.utils import timezone
from django.db import models

# The Question model represents a poll with question, answers, and votes. It has
# a many-to-many relationship with the UserData model. See
# qsource-user/models.py to see the details of the UserData model
# implementation.
class Question(models.Model):
    # Basic poll information.
    question_text = models.CharField(max_length = 300)    
    ans1_text = models.CharField(max_length = 80, default= "Yes")
    ans1_votes = models.IntegerField(default = 0)
    ans2_text = models.CharField(max_length = 80, default = "No")
    ans2_votes = models.IntegerField(default = 0)
    
    # Store the publication date so that questions are able to be sorted by most
    # recently asked listed first.
    pub_date = models.DateTimeField('date published')
    # Store the total votes on each question so that questions can be sored by
    # popularity.
    votes = models.IntegerField(default = 0)
    
    # Generate a string to represent the Question object
    def __unicode__(self):
        return self.question_text
    
    # Return true or false depending on if the question was asked in the last
    # day.
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    # Specifications for the appearance of the was_published_recently attribute
    # on QSoure's admin site.
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    # A question manages its own data by tallying new votes via a member
    # function.
    def vote(self, ans_num):
        if(int(ans_num) == 0): 
            self.ans1_votes += 1    
        elif(int(ans_num) == 1): 
            self.ans2_votes += 1
        self.votes = self.ans1_votes + self.ans2_votes
