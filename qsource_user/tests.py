from django.test import TestCase
from django.core.urlresolvers import reverse
from polls.models import Question
from qsource_user.models import *
from django.contrib.auth.models import User
from django.test import Client
import datetime
from django.utils import timezone

def create_question_time(question_text, days):

    # Creates a question with the given `question_text` published the given
    # number of `days` offset to now (negative for questions published
    # in the past, positive for questions that have yet to be published).

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)

def create_question(question_text, ans1, ans2):
    # Creates a question published now with custom answer choices
    return Question.objects.create(question_text=question_text,
                                   pub_date = timezone.now(),
                                   ans1_text = ans1,
                                   ans2_text = ans2)


class UserDataTests(TestCase):

    def test_create_data_from_user(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        self.assertEqual(newUser.pk, newData.pk)
        self.assertEqual(newData, newUser.data)

    def test_cannot_answer_twice(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newQ = create_question("Anybody out there?", "yes", "no")
        newData.answer(newQ, 0)
        newData.answer(newQ, 1)
        self.assertEqual(newQ.ans1_votes, 1)
        self.assertEqual(newQ.votes, 1)
    

class UserViewTests(TestCase):

    # def test_update_settings_none(self):
    
    # def test_update_settings_single(self):
    
    # def test_update_settings_all(self):
    
    # def test_recent(self):
    
    # def test_popular(self):
    
    def test_my(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        newQ = create_question_time("Not my question.", -1)
        newData.ask("My question.", "Yes", "No")
        newData.showMyQuestions = True
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>']
        )
        
    
