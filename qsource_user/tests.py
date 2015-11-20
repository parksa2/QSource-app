from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
from polls.views import get_data_or_create

#Test that questions are added to the QuestionsAnswered database table and are
#properly assocaited with the user that answered the question.
class QuestionsAnsweredTests(TestCase):
    def test_questions_answered_object_added(self):
        NewUser = User.objects.create_user('test', 'test@test.com', '12345')
        NewUserData = UserData.objects.create(user = NewUser)
        NewUser.is_active = True
        c = Client()
        c.login(username = 'test', password = '12345')
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
        NewUser = User.objects.create_user('test', 'test@test.com', '12345')
        NewUserData = UserData.objects.create(user = NewUser)
        NewUser.is_active = True
        c = Client()
        c.login(username = 'test', password = '12345')
        #Create a new question and add it to the Question and QuestionAsked
        #database tables.
        NewUserData.ask('Fish?', 'Yes', 'No')
        #Retrieve the question from the QuestionAsked database table
        QuestionsAskedByTestUser = QuestionsAsked.objects.filter(user =
                                                            NewUserData)
        #Should be a list containing one entry as one questions was asked by
        #the user.
        self.assertEqual(len(QuestionsAskedByTestUser), 1)
