from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic 
from .models import Question
from django.shortcuts import redirect
from qsource_user.models import UserData
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

    def get_queryset(self):        
        if(self.user_data.showRecent):
            return self.get_all_global_recent()
        else:
            return self.get_all_global_popular()
            
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

    ans_num = (request.POST['ans'])
    if(int(ans_num) == 0): 
        p.ans1_votes += 1    
    else: 
        p.ans2_votes += 1
    p.votes = p.ans1_votes + p.ans2_votes
    p.save()
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    
def get_data_or_create(myuser):
    if(hasattr(myuser, 'data') != True):
        #generate a default and proceed
        thisUser = UserData.objects.create(user = myuser)
        thisUser.save()
        return thisUser
        
    else:
        return myuser.data
    
def settings(request):
    opt_str = (request.POST['opt'])
    thisUser = get_data_or_create(request.user)
        
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

  

        
        
        