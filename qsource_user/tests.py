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
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        #Check correct associations
        self.assertEqual(newUser.pk, newData.pk)
        self.assertEqual(newUser, newData.user)
        self.assertEqual(newData, newUser.data)

    def test_cannot_answer_twice(self):
        #Check behavior for duplicate answer attempts
        #Should block a second vote, even if the other choice is selected
        newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        newData = UserData.objects.create(user = newUser)
        newQ = create_question("Anybody out there?", "yes", "no")
        newData.answer(newQ, 0)
        newData.answer(newQ, 1)
        #Make sure the correct vote, and only the correct vote, has been registered
        self.assertEqual(newQ.ans1_votes, 1)
        self.assertEqual(newQ.ans2_votes, 0)
        self.assertEqual(newQ.votes, 1)
        #Make sure the database hasn't stored an extra QuestionsAnswered object
        numAnsweredObjects = len(QuestionsAnswered.objects.filter(
            user = newData, 
            questionID = newQ.pk))
        self.assertEqual(numAnsweredObjects, 1)

#helper function to simluate authentication of new user
#allows UserData to interact with view
def new_user_login(client):
    newUser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    newData = UserData.objects.create(user = newUser)
    newUser.is_active = True
    client.login(username = 'john', password = 'johnpassword')
    return newUser

class UserViewTests(TestCase):

    #Test Menu submission with no changed options
    def test_update_settings_none(self):
        c = Client()
        newUser = new_user_login(c)
        c.post('/polls/settings/', {})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, False)
        self.assertEqual(newData.showLocal, False)
        self.assertEqual(newData.showRecent, True)
    
    #Test menu submission with a single changed option
    def test_update_settings_single(self):
        c = Client()
        newUser = new_user_login(c)
        c.post('/polls/settings/', {'opt1':'My'})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, True)
        self.assertEqual(newData.showLocal, False)
        self.assertEqual(newData.showRecent, True)
     
    #test menu submission with all options changed
    def test_update_settings_all(self):
        c = Client()
        newUser = new_user_login(c)
        c.post('/polls/settings/', {'opt1':'My', 'opt2':'Local', 'opt3':'Popular'})
        newData = UserData.objects.get(pk = newUser.pk)
        self.assertEqual(newData.showMyQuestions, True)
        self.assertEqual(newData.showLocal, True)
        self.assertEqual(newData.showRecent, False)

    #test showRecent = True feed setting
    def test_recent(self):
        c = Client()
        newUser = new_user_login(c)
        newData = UserData.objects.get(pk = newUser.pk)
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

    #test showRecent = False setting (sort by most votes)
    def test_popular(self):
        c = Client()
        newUser = new_user_login(c)
        newData = UserData.objects.get(pk = newUser.pk)
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
    
    #test showMyQuestions = True (questions asked by this user only)
    def test_my(self):
        c = Client()
        newUser = new_user_login(c)
        newData = UserData.objects.get(pk = newUser.pk)
        newQ = create_question_time("Not my question.", -1)
        newData.ask("My question.", "Yes", "No")
        newData.showMyQuestions = True
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>']
        )
    
    #test showMyQuestions = False (all applicable questions shown)
    def test_all(self):
        c = Client()
        newUser = new_user_login(c)
        newData = UserData.objects.get(pk = newUser.pk)
        newQ = create_question_time("Not my question.", -1)
        newData.ask("My question.", "Yes", "No")
        newData.showMyQuestions = False
        newData.save()
        response = c.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: My question.>', '<Question: Not my question.>']
        )
                
    
#Test that questions are added to the QuestionsAnswered database table and are
#properly associated with the user that answered the question.
class QuestionsAnsweredTests(TestCase):
    def test_questions_answered_object_added(self):
        c = Client()
        NewUser = new_user_login(c)
        NewUserData = UserData.objects.get(pk = NewUser.pk)
        TestQuestion = Question.objects.create(question_text = 'Fish?',
                                               ans1_text = 'Yes',
                                               ans2_text = 'No',
                                               pub_date = timezone.now())
        Response = NewUserData.answer(TestQuestion, 0)
        QuestionsAnsweredByNewUser = QuestionsAnswered.objects.filter(user =
                                                            NewUserData)
        #Response should be "True" because the questions has not been answered
        #by the user before.
        self.assertEqual(Response, True)
        #Should be a list containing one entry as one questions was answered by
        #the user.
        self.assertEqual(len(QuestionsAnsweredByNewUser), 1)

#Test that questions are added to the QuestionsAsked database table and are
#properly assocaited with the user that asked the question.
class QuestionsAskedTests(TestCase):
    def test_questions_asked_object_added(self):
        c = Client()
        NewUser = new_user_login(c)
        NewUserData = UserData.objects.get(pk = NewUser.pk)
        #Create a new question and add it to the Question and QuestionAsked
        #database tables.
        NewUserData.ask('Fish?', 'Yes', 'No')
        #Retrieve the question from the QuestionAsked database table
        QuestionsAskedByTestUser = QuestionsAsked.objects.filter(user =
                                                            NewUserData)
        #Should be a list containing one entry as one questions was asked by
        #the user.
        self.assertEqual(len(QuestionsAskedByTestUser), 1)
