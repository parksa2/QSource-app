from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic 
from .models import Question
from .forms import QuestionForm
from django.shortcuts import redirect
from qsource_user.models import *
from django.contrib.auth.models import User

# Main view for the app that loads the question feed according to the user's
# settings.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'    
    # Because get_queryset and get_context_data do not access the request,
    # the relevant user data is stored in a member variable by get().
    user_data = 0

    # Extend the inherited get() function by redirecting if not logged in
    # and saving user's settings.
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            self.user_data = get_data_or_create(request.user)
            return super(IndexView, self).get(self, request, *args, **kwargs)
    
    # Extend inherited get_context_data by adding additional context varibles
    # representing user settings. This allows the HTML to access the user's
    # options for menu display puposes.
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_my'] = self.user_data.showMyQuestions
        context['user_local'] = self.user_data.showLocal
        context['user_recent'] = self.user_data.showRecent
        return context

    # Specify the list of questions to display. Choose appropriate sort/filter
    # functions based on user settings.
    def get_queryset(self):        
        if(self.user_data.showRecent):
            if(self.user_data.showMyQuestions):
                return self.get_my_global_recent()
            else:
                return self.get_all_global_recent()
        else:
            if(self.user_data.showMyQuestions):
                return self.get_my_global_popular()
            else:
                return self.get_all_global_popular()
            
    
    # Return the questions asked by this user, most recent first.
    def get_my_global_recent(self):
        my_questions = QuestionsAsked.objects.filter(
            user = self.user_data
        )
        return Question.objects.filter(
            pk__in = [my_q.questionID for my_q in my_questions],
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]
    
    # Return the questions asked by this user, most popular first.
    def get_my_global_popular(self):
        my_questions = QuestionsAsked.objects.filter(
            user = self.user_data
        )
        return Question.objects.filter(
            pk__in = [my_q.questionID for my_q in my_questions],
            pub_date__lte=timezone.now()
        ).order_by('-votes')[:10]
    
    # Return the most voted on 10 questions in the database.
    def get_all_global_popular(self):
        return Question.objects.filter( 
            pub_date__lte=timezone.now()
        ).order_by('-votes')[:10]
    
    # Return the most recent 10 questions in the database.
    def get_all_global_recent(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]

# View and vote on a single question.
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            return super(DetailView, self).get(self, request,*args, **kwargs)
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

# Show the results for a single question.
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)    
        context['already_answered'] = False
        return context
        
    def get(self, request, *args, **kwargs):
        user_data = get_data_or_create(request.user)
        
        if (not request.user.is_authenticated()
            or not QuestionsAnswered.objects.filter(
                user = user_data, 
                questionID = self.get_object().pk
            ).exists()
        ):
            return redirectHome()
        else:
            return super(ResultsView, self).get(self, request, *args, **kwargs)
    
# Handle POST requests for a new vote. This function is called from form in 
# index.html or detail.html  
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    user_data = get_data_or_create(request.user)
    ans_num = request.POST.get('ans', -1)
    # Responsibility for modifying data is passed off to the relevant UserData
    # instance.
    success = user_data.answer(p, ans_num)  
    if(success):
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    else:
        return render( request, 'polls/results.html', {'already_answered':True, 'question':p})

# Handle recieving a request to publish a new question
def GetQuestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            # Get info from request
            new_question_text = form.cleaned_data.get("question_text")            
            option1 = form.cleaned_data.get("option1")            
            option2 = form.cleaned_data.get("option2")         
            user_data = get_data_or_create(request.user)
            # Pass off responsibility for new question creation to UserData
            user_data.ask(new_question_text, option1, option2)
            return HttpResponseRedirect('/polls/')
    else:
        form = QuestionForm()
    return render(request, 'question.html', {'form': form})
    
# Return a user's data or, if this is the first time the feed is loaded,
# generate a new UserData object with default settings.
def get_data_or_create(myuser):
    if(hasattr(myuser, 'data') != True):
        #generate a default and proceed
        thisUser = UserData.objects.create(user = myuser)
        thisUser.save()
        return thisUser
        
    else:
        return myuser.data
 
# Change any number of user settings. This function is called from form in 
# index.html
def settings(request):
    # Get all required info from the request.
    opt1_str = request.POST.get('opt1', "")
    opt2_str = request.POST.get('opt2', "")
    opt3_str = request.POST.get('opt3', "")
    thisUser = get_data_or_create(request.user)
    # Change the appropriate settings based on the infor received from the
    # request.
    if(opt1_str == "My"):
        thisUser.showMyQuestions = True
    elif(opt1_str == "All"):
        thisUser.showMyQuestions = False
    if(opt2_str == "Local"):
        thisUser.showLocal = True
    elif(opt2_str == "Global"):
        thisUser.showLocal = False
    if(opt3_str == "Recent"):
        thisUser.showRecent = True
    elif(opt3_str == "Popular"):
        thisUser.showRecent = False        
    thisUser.save()
    return redirect('polls:index', permanent = True)
    
# Redirect a user to the homepage when the user is not logged in.
def redirectHome():
    return redirect('home', permanent = True)
