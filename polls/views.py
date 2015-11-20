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


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'    
    user_data = 0

    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            self.user_data = get_data_or_create(request.user)
            
            return super(IndexView, self).get(self, request, *args, **kwargs)
            
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_my'] = self.user_data.showMyQuestions
        context['user_local'] = self.user_data.showLocal
        context['user_recent'] = self.user_data.showRecent
        return context

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
            
           
    def get_my_global_recent(self):
        my_questions = QuestionsAsked.objects.filter(user = self.user_data)
        return Question.objects.filter(pk__in = [my_q.questionID for my_q in my_questions]).order_by('-pub_date')[:10]
        
    def get_my_global_popular(self):
        my_questions = QuestionsAsked.objects.filter(user = self.user_data)
        return Question.objects.filter(pk__in = [my_q.questionID for my_q in my_questions]).order_by('-votes')[:10]
        
    def get_all_global_popular(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-votes')[:10]
        
    def get_all_global_recent(self):
        #"""Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]

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

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            return super(ResultsView, self).get(self, request, *args, **kwargs)
    
    
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    user_data = get_data_or_create(request.user)
    ans_num = (request.POST['ans'])
    user_data.answer(p, ans_num)  
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def GetQuestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            new_question_text = form.cleaned_data.get("question_text")            
            option1 = form.cleaned_data.get("option1")            
            option2 = form.cleaned_data.get("option2")         
            user_data = get_data_or_create(request.user)
            user_data.ask(new_question_text, option1, option2)
            return HttpResponseRedirect('/polls/')
    else:
        form = QuestionForm()
    return render(request, 'question.html', {'form': form})
    
def get_data_or_create(myuser):
    if(hasattr(myuser, 'data') != True):
        #generate a default and proceed
        thisUser = UserData.objects.create(user = myuser)
        thisUser.save()
        return thisUser
        
    else:
        return myuser.data
    
def settings(request):
    opt1_str = request.POST.get('opt1', "")
    opt2_str = request.POST.get('opt2', "")
    opt3_str = request.POST.get('opt3', "")
    thisUser = get_data_or_create(request.user)
        
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
    return redirect('home', permanent = True)
    
def redirectHome():
    return redirect('home', permanent=True)
