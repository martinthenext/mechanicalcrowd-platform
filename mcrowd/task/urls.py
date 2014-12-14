from django.conf.urls import patterns, url
from .views import TasksView, TaskView, TableView


urlpatterns = (
    url(r'^$', TasksView.as_view()),
    url(r'^(?P<pk>\d+)/$', TaskView.as_view()),
    url(r'^(?P<pk>\d+)/table/$', TableView.as_view()),
)
