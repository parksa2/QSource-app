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
        #Check correct associations
        self.assertEqual(new_user.pk, new_data.pk)
        self.assertEqual(new_user, new_data.user)
        self.assertEqual(new_data, new_user.data)

    def test_cannot_answer_twice(self):
        #Check behavior for duplicate answer attempts
        #Should block a second vote, even if the other choice is selected
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_data = UserData.objects.create(user = new_user)
        newQ = create_question("Anybody out there?", "yes", "no")
        new_data.answer(newQ, 0)
        new_data.answer(newQ, 1)
        #Make sure the correct vote, and only the correct vote, has been registered
        self.assertEqual(newQ.ans1_votes, 1)
        self.assertEqual(newQ.ans2_votes, 0)
        self.assertEqual(newQ.votes, 1)
        #Make sure the database hasn't stored an extra QuestionsAnswered object
        numAnsweredObjects = len(QuestionsAnswered.objects.filter(
            user = new_data, 
            questionID = newQ.pk))
        self.assertEqual(numAnsweredObjects, 1)

#helper function to simluate authentication of new user
#allows UserData to interact with view
def new_user_login(client):
    new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    new_data = UserData.objects.create(user = new_user)
    new_user.is_active = True
    client.login(username = 'john', password = 'johnpassword')
    return new_user

class UserViewTests(TestCase):

    #Test Menu submission with no changed options
    def test_update_settings_none(self):
        c = Client()
        new_user = new_user_login(c)
        c.post('/polls/settings/', {})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, False)
        self.assertEqual(new_data.showLocal, False)
        self.assertEqual(new_data.showRecent, True)
    
    #Test menu submission with a single changed option
    def test_update_settings_single(self):
        c = Client()
        new_user = new_user_login(c)
        c.post('/polls/settings/', {'opt1':'My'})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, True)
        self.assertEqual(new_data.showLocal, False)
        self.assertEqual(new_data.showRecent, True)
     
    #test menu submission with all options changed
    def test_update_settings_all(self):
        c = Client()
        new_user = new_user_login(c)
        c.post('/polls/settings/', {'opt1':'My', 'opt2':'Local', 'opt3':'Popular'})
        new_data = UserData.objects.get(pk = new_user.pk)
        self.assertEqual(new_data.showMyQuestions, True)
        self.assertEqual(new_data.showLocal, True)
        self.assertEqual(new_data.showRecent, False)

    #test showRecent = True feed setting
    def test_recent(self):
        c = Client()
        new_user = new_user_login(c)
        new_data = UserData.objects.get(pk = new_user.pk)
        newQ1 = create_question_time("Old.", -1)
        new_data.answer(newQ1, 0)
        newQ2 = create_question_time("New.", 0)
        new_data.showRecent = True
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: New.>','<Question: Old.>']
        ) 

    #test showRecent = False setting (sort by most votes)
    def test_popular(self):
        c = Client()
        new_user = new_user_login(c)
        new_data = UserData.objects.get(pk = new_user.pk)
        newQ1 = create_question_time("Has votes.", -1)
        new_data.answer(newQ1, 0)
        newQ2 = create_question_time("No votes.", 0)
        new_data.showRecent = False
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Has votes.>','<Question: No votes.>']
        )
    
    #test showMyQuestions = True (questions asked by this user only)
    def test_my(self):
        c = Client()
        new_user = new_user_login(c)
        new_data = UserData.objects.get(pk = new_user.pk)
        newQ = create_question_time("Not my question.", -1)
        new_data.ask("My question.", "Yes", "No")
        new_data.showMyQuestions = True
        new_data.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>']
        )
    
    #test showMyQuestions = False (all applicable questions shown)
    def test_all(self):
        c = Client()
        new_user = new_user_login(c)
        new_data = UserData.objects.get(pk = new_user.pk)
        newQ = create_question_time("Not my question.", -1)
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
        c = Client()
        new_user = new_user_login(c)
        new_user_data = UserData.objects.get(pk = new_user.pk)
        TestQuestion = Question.objects.create(question_text = 'Fish?',
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
        c = Client()
        new_user = new_user_login(c)
        new_user_data = UserData.objects.get(pk = new_user.pk)
        #Create a new question and add it to the Question and QuestionAsked
        #database tables.
        new_user_data.ask('Fish?', 'Yes', 'No')
        #Retrieve the question from the QuestionAsked database table
        QuestionsAskedByTestUser = QuestionsAsked.objects.filter(user =
                                                            new_user_data)
        #Should be a list containing one entry as one questions was asked by
        #the user.
