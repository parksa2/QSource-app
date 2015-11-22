from django.conf.urls import url

from . import views 

# Regular expressions that determine the possible patterns that a URL can match.
# If a URL matches one of the given patterns, the appropriate method is called.
urlpatterns = [
    
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^question/$', views.GetQuestion, name='question'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^settings/$', views.settings, name='settings')

]


