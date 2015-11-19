from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic 
from .models import Question
from .forms import QuestionForm
from django.shortcuts import redirect
from qsource_user.models import UserData
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'    
    def get_queryset(self):
        

    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            return super(IndexView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):        
        #"""Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated() != True):
            return redirectHome()
        else:
            return super(DetailView, self).get(self, request,*args, **kwargs)
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
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

    ans_num = (request.POST['ans'])
    if(int(ans_num) == 0): 
        p.ans1_votes += 1    
    else: 
        p.ans2_votes += 1
    p.save()
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def GetQuestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            new_question_text = form.cleaned_data.get("question_text")            
            option1 = form.cleaned_data.get("option1")            
            option2 = form.cleaned_data.get("option2")            
            NewQuestion = Question()
            NewQuestion.question_text = new_question_text
            NewQuestion.ans1_text = option1
            NewQuestion.ans2_text = option2
            NewQuestion.pub_date = timezone.now()
            NewQuestion.save()
            return HttpResponseRedirect('/polls/')
    else:
        form = QuestionForm()
    return render(request, 'question.html', {'form': form})
    
def settings(request):
    opt_str = (request.POST['opt'])
    thisUser = 0
    if(hasattr(request.user, 'data') != True):
        #generate a default and proceed
        thisUser = UserData.objects.create(user = request.user)
        thisUser.save()
        
    thisUser = request.user.data
        
    if(opt_str == "My"):
        thisUser.showMyQuestions = True
    elif(opt_str == "All"):
        thisUser.showMyQuestions = False
    elif(opt_str == "Local"):
        thisUser.showLocal = True
    elif(opt_str == "Global"):
        thisUser.showLocal = False
    elif(opt_str == "Recent"):
        thisUser.showRecent = True
    elif(opt_str == "Popular"):
        thisUser.showRecent = False        
    thisUser.save()
    return redirect('home', permanent = True)
    
def redirectHome():
    return redirect('home', permanent=True)
