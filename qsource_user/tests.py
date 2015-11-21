from django.core.urlresolvers import reverse
from polls.models import Question
from qsource_user.models import *
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.test import TestCase, Client
from .models import *
from polls.views import get_data_or_create

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
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        self.assertEqual(new_user.pk, new_data.pk)
        self.assertEqual(new_data, new_user.data)

    def test_cannot_answer_twice(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_q = create_question("Anybody out there?", "yes", "no")
        new_data.answer(new_q, 0)
        new_data.answer(new_q, 1)
        self.assertEqual(new_q.ans1_votes, 1)
        self.assertEqual(new_q.votes, 1)
    

class UserViewTests(TestCase):

    def test_update_settings_none(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, False)
        self.assertEqual(new_data.showLocal, False)
        self.assertEqual(new_data.showRecent, True)
    
    def test_update_settings_single(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {'opt1':'My'})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, True)
        self.assertEqual(new_data.showLocal, False)
        self.assertEqual(new_data.showRecent, True)
        
    def test_update_settings_all(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        c.post('/polls/settings/', {'opt1':'My', 'opt2':'Local', 'opt3':'Popular'})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, True)
        self.assertEqual(new_data.showLocal, True)
        self.assertEqual(new_data.showRecent, False)
    
    def test_recent(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        new_q1 = create_question_time("Old.", -1)
        new_data.answer(new_q1, 0)
        new_q2 = create_question_time("New.", 0)
        new_data.showRecent = True
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: New.>','<Question: Old.>']
        ) 

        
    def test_popular(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        new_q1 = create_question_time("Has votes.", -1)
        new_data.answer(new_q1, 0)
        new_q2 = create_question_time("No votes.", 0)
        new_data.showRecent = False
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Has votes.>','<Question: No votes.>']
        )
    
    def test_my(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        new_q = create_question_time("Not my question.", -1)
        new_data.ask("My question.", "Yes", "No")
        new_data.showMyQuestions = True
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>']
        )

    def test_all(self):
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'john', password = 'johnpassword')
        new_q = create_question_time("Not my question.", -1)
        new_data.ask("My question.", "Yes", "No")
        new_data.showMyQuestions = False
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>', '<Question: Not my question.>']
        )
                
    
# Test that questions are added to the QuestionsAnswered database table and are
# properly associated with the user that answered the question.
class QuestionsAnsweredTests(TestCase):
    def test_questions_answered_object_added(self):
        new_user = User.objects.create_user('test', 'test@test.com', '12345')
        new_user_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'test', password = '12345')
        test_question = Question.objects.create(question_text = 'Fish?',
                                               ans1_text = 'Yes',
                                               ans2_text = 'No',
                                               pub_date = timezone.now())
        response = new_user_data.answer(test_question, 0)
        questions_answered_by_new_user = QuestionsAnswered.objects.filter(user =
                                                            new_user_data)
        # Response should be "True" because the questions has not been answered
        # by the user before.
        self.assertEqual(response, True)
        # Should be a list containing one entry as one questions was answered by
        # the user.
        self.assertEqual(len(questions_answered_by_new_user), 1)

# Test that questions are added to the QuestionsAsked database table and are
# properly assocaited with the user that asked the question.
class QuestionsAskedTests(TestCase):
    def test_questions_asked_object_added(self):
        new_user = User.objects.create_user('test', 'test@test.com', '12345')
        new_user_data = UserData.objects.create(user = new_user)
        new_user.is_active = True
        c = Client()
        c.login(username = 'test', password = '12345')
        # Create a new question and add it to the Question and QuestionAsked
        # database tables.
        new_user_data.ask('Fish?', 'Yes', 'No')
        # Retrieve the question from the QuestionAsked database table.
        questions_asked_by_test_user = QuestionsAsked.objects.filter(user =
                                                            new_user_data)
        # Should be a list containing one entry as one questions was asked by
        # the user.
        self.assertEqual(len(questions_asked_by_test_user), 1)
