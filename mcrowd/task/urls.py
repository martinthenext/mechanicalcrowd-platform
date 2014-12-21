from django.conf.urls import patterns, url
from .views import TasksView, TaskView
from .views import OriginalRowsView, RowDiffView


urlpatterns = (
    url(r'^$', TasksView.as_view(), name='task'),
    url(r'^(?P<pk>\d+)/$', TaskView.as_view(), name='tasks'),
    url(r'^(?P<pk>\d+)/table/$', OriginalRowsView.as_view(), name='original'),
    url(r'^(?P<pk>\d+)/diff/$', RowDiffView.as_view(), name='diff'),
)
