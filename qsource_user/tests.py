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

    def test_update_settings_none(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, False)
        self.assertEqual(newData.showLocal, False)
        self.assertEqual(newData.showRecent, True)
    
    def test_update_settings_single(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {'opt1':'My'})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, True)
        self.assertEqual(newData.showLocal, False)
        self.assertEqual(newData.showRecent, True)
        
    def test_update_settings_all(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {'opt1':'My', 'opt2':'Local', 'opt3':'Popular'})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, True)
        self.assertEqual(newData.showLocal, True)
        self.assertEqual(newData.showRecent, False)
    
    def test_recent(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        newQ1 = create_question_time("Old.", -1)
        newData.answer(newQ1, 0)
        newQ2 = create_question_time("New.", 0)
        newData.showRecent = True
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: New.>','<Question: Old.>']
        ) 

        
    def test_popular(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        newQ1 = create_question_time("Has votes.", -1)
        newData.answer(newQ1, 0)
        newQ2 = create_question_time("No votes.", 0)
        newData.showRecent = False
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Has votes.>','<Question: No votes.>']
        )
    
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

    def test_all(self):
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newUser.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        newQ = create_question_time("Not my question.", -1)
        newData.ask("My question.", "Yes", "No")
        newData.showMyQuestions = False
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>', '<Question: Not my question.>']
        )
                
    
