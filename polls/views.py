from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic 
from .models import Question
from django.shortcuts import redirect


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'    

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
    
def redirectHome():
    return redirect('home', permanent=True)

    

        
        
        